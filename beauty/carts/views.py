import json

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic import View
from django_redis import get_redis_connection

from beauty.settings import PIC_URL
from goods.models import *
from utils.loging_decorator import logging_check
from django.conf import settings

redis_conn = get_redis_connection('cart')


class CartsView(View):
    # 所有视图类的请求，都会第一个执行该方法
    @logging_check
    def dispatch(self, request, *args, **kwargs):
        json_str = request.body
        request.json_obj = {}
        if json_str:
            json_obj = json.loads(json_str)
            request.json_obj = json_obj
        request.sku = None
        if 'sku_id' in request.json_obj:
            try:
                sku = SKU.objects.get(id=request.json_obj['sku_id'])
            except Exception as e:
                return None
            request.sku = sku
        return super().dispatch(request, *args, **kwargs)

    def get_cache_key(self, user_id):
        return 'cart_%s' % (user_id)

    def get_carts_data(self, user_id):
        # 获取用户redis中的购物车数据，转成字典格式
        key = self.get_cache_key(user_id)
        o_data = redis_conn.hgetall(key)
        if not o_data:
            return {}
        data = {int(k): json.loads(v) for k, v in o_data.items()}
        return data

    def del_cart_data(self, user_id, sku_id):
        redis_conn.hdel('cart_%d' % user_id, sku_id)

    def get_cart_data(self, user_id, sku_id):
        key = self.get_cache_key(user_id)
        value = redis_conn.hget(key, sku_id)
        if not value:
            return None
        return json.loads(value)

    def set_carts_data(self, user_id, sku_id, data):
        # 存储用户购物车数据进redis

        # data是字典形式，存redis之前要序列化
        data_s = json.dumps(data)
        key = self.get_cache_key(user_id)
        redis_conn.hset(key, sku_id, data_s)

    def set_select_unselect(self, user_id, sku_id, selected):
        cart = self.get_cart_data(user_id, sku_id)
        if not cart:
            return None

        info = {'count': cart['count'], 'selected': selected}
        self.set_carts_data(user_id, sku_id, info)

    def set_selectall_unselectall(self, user_id, selected):
        carts = self.get_carts_data(user_id)
        if not carts:
            return None
        for sku_id, data in carts.items():
            info = {'count': data['count'], 'selected': selected}
            self.set_carts_data(user_id, sku_id, info)
        skus_list = self.get_cart_list(user_id)
        return skus_list

    def get_cart_list(self, user_id):
        # 获取用户购物车数据[前端要求]
        # [{"id":"","name":"","cart_count":"","selected":"","default_image_url":"","price":"","sku_sale_attr_name":[],"sku_sale_attr_val":[]},{"":""...}]
        # 先取出redis中的购物车数据
        cart_dict = self.get_carts_data(user_id)
        # {3:{'count':1,'selected':1}}
        skus = SKU.objects.filter(id__in=cart_dict.keys())
        sku_list = []
        for sku in skus:
            sku_dict = {}
            sku_dict['id'] = sku.id
            sku_dict['name'] = sku.name
            sku_dict['cart_count'] = int(cart_dict[sku.id]['count'])
            sku_dict['selected'] = int(cart_dict[sku.id]['selected'])
            sku_dict['default_image_url'] = str(sku.default_image_url)
            sku_dict['price'] = sku.price
            sku_sale_attr_name = []
            sku_sale_attr_value = []
            saleattr_vals = SaleAttrValue.objects.filter(sku=sku)
            for saleattr in saleattr_vals:
                sku_sale_attr_value.append(saleattr.sale_attr_value_name)
                sku_sale_attr_name.append(saleattr.sale_attr_id.sale_attr_name)
            sku_dict['sku_sale_attr_name'] = sku_sale_attr_name
            sku_dict['sku_sale_attr_val'] = sku_sale_attr_value
            sku_list.append(sku_dict)
        return sku_list

    def get_sku_name_and_values(self,sku_id):
        sku_sale_attr_name=[]
        sku_sale_attr_val=[]
        sales=SaleAttrValue.objects.filter(sku_id=sku_id).select_related('sale_attr_id').only('sale_attr_value_name','sale_attr_id__sale_attr_name').values('sale_attr_value_name','sale_attr_id__sale_attr_name')
        for sale in sales:
            sku_sale_attr_name.append(sale['sale_attr_id__sale_attr_name'])
            sku_sale_attr_val.append(sale['sale_attr_value_name'])
        return sku_sale_attr_val,sku_sale_attr_name


    def del_cart_data(self, user_id, sku_id):
        redis_conn.hdel('cart_%d' % user_id, sku_id)

    def post(self, request, username):
        count = request.json_obj['cart_count']
        uid = request.user.id
        sku = request.sku

        if not sku:
            return JsonResponse({'code': 30102, 'error': '没有sku参数'})
        if request.user.username != username:
            return JsonResponse({'code': 30104, 'error': '非登录者用户'})

        try:
            count = int(count)
        except Exception as e:
            print(e)
            return JsonResponse({'code': 30102, 'error': "传参不正确"})
        if count > sku.stock:
            return JsonResponse({'code': 9999, 'error': '超量'})

        carts = self.get_carts_data(uid)
        if not carts:
            info = {'count': count, 'selected': 1}
            self.set_carts_data(uid, sku.id, info)
            cart_data = self.get_carts_data(uid)
            count = len(cart_data)
            return JsonResponse({'code': 200, 'data': {'cart_count': count}, 'base_url': PIC_URL})
        else:
            my_sku_info = carts.get(sku.id)
            if not my_sku_info:
                my_sku_info = {'count': count, 'selected': 1}
            else:
                old_count = my_sku_info['count']
                new_count = old_count + count
                if new_count > sku.stock:
                    return JsonResponse({'code': 9999, 'error': '超量'})
                my_sku_info['count'] = new_count

            self.set_carts_data(uid, sku.id, my_sku_info)
            cart_data = self.get_carts_data(uid)
            count = len(cart_data)
            return JsonResponse({'code': 200, 'data': {'cart_count': count}, 'base_url': PIC_URL})

    def get(self, request, username):
        # 获取用户购物车数据
        sku_list = self.get_cart_list(request.user.id)
        return JsonResponse({'code': 200, 'data': sku_list, 'base_url': settings.PIC_URL})

    def delete(self, request, username):
        sku = request.sku
        user = request.user
        if not sku:
            return JsonResponse({'code': 30102, 'error': '没有sku参数'})
        if user.username != username:
            return JsonResponse({'code': 30104, 'error': '非登录者用户'})
        self.del_cart_data(user.id,sku.id)
        carts_data = self.get_carts_data(user.id)
        # count 是redis现存的sku的数量
        count=len(carts_data)
        return JsonResponse({'code': 200, 'data': {'cart_count': count}, 'base_url': PIC_URL})
