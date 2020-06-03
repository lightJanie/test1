import json
from datetime import datetime

from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views import View
from django_redis import get_redis_connection

from beauty.settings import PIC_URL
from carts.views import CartsView
from goods.models import SKU
from order.models import OrderInfo, OrderGoods
from user.models import Address
from utils.loging_decorator import logging_check


class OrderBaseView(View):
    def get_cart_dict(self,user_id):
        cart_dict=CartsView().get_carts_data(user_id)
        return cart_dict

    def get_address(self,user_id):
        addresses=Address.objects.filter(uid_id=user_id,isActive=True)
        print(addresses)
        addresses_default=[]
        addresses_no_default=[]
        for address in addresses:
            if address.default_address ==True:
                addresses_default.append({
                    'id':address.id,
                    'name':address.receiver,
                    'mobile':address.receiver_mobile,
                    'title':address.tag,
                    'address':address.address
                })
            else:
                addresses_no_default.append({
                    'id': address.id,
                    'name': address.receiver,
                    'mobile': address.receiver_mobile,
                    'title': address.tag,
                    'address': address.address
                })
        return addresses_default+addresses_no_default

    def get_cart_order_list(self,user_id):
        sku_list=[]
        skus_list=CartsView().get_cart_list(user_id)
        if skus_list:
            for sku_info in skus_list:
                if sku_info['selected']==1:
                    sku_list.append(sku_info)

        return sku_list

    # 获取立即购买的商品列表
    def get_direct_order_list(self,sku_ids,count):
        sku_list=[]
        for sku in sku_ids:
            sku_sale_attr_val, sku_sale_attr_name = CartsView().get_sku_name_and_values(sku.id)
            sku_list.append({
                'id': sku.id,
                'default_image_url': str(sku.default_image_url),
                'name': sku.name,
                'price': sku.price,
                'cart_count': count,
                'total_amount': sku.price * int(count),
                "sku_sale_attr_name": sku_sale_attr_name,
                "sku_sale_attr_val": sku_sale_attr_val,
            })
        return sku_list

    def delete_redis_order(self,sku_ids,user_id):
        redis_cli=get_redis_connection('cart')
        for sku_id in sku_ids:
            redis_cli.hdel('cart_%d'%user_id,sku_id)


class AdvanceOrderView(OrderBaseView):
    @logging_check
    def get(self,request,username):
        user=request.user
        addresses_list=self.get_address(user.id)
        settlement=int(request.GET.get('settlement_type'))
        if settlement==0:
            sku_list=self.get_cart_order_list(user.id)
            print('购物车',sku_list)
        elif settlement==1:
            sku_id=request.GET.get('sku_id')
            count=request.GET.get('buy_num')
            skus=SKU.objects.filter(id=sku_id)
            sku_list=self.get_direct_order_list(skus,count)
            print('立刻购买',sku_list)

        data={
            'addresses':addresses_list,
            'sku_list':sku_list
        }

        return JsonResponse({'code': 200, 'data': data, 'base_url': PIC_URL})


class OrderInfoView(OrderBaseView):
    @logging_check
    def post(self,request,username):
        user=request.user
        address_id=json.loads(request.body).get('address_id')
        try:
            address=Address.objects.get(id=address_id)
        except:
            return JsonResponse({'code': 50102, 'errmsg': '收货地址无效'})
        now=datetime.now()

        with transaction.atomic():
            sid=transaction.savepoint()
            order_id='%s%02d'%(now.strftime('%Y%m%d%H%M%s'),user.id)
            total_count=0
            total_amount=0
            order=OrderInfo.objects.create(
                order_id=order_id,
                user_id=user.id,
                address=address.id,
                receiver=address.receiver,
                receiver_mobile=address.receiver_mobile,
                tag=address.tag,
                total_count=0,
                total_amount=0,
                freight=10,
                pay_method=1,
                status=1
            )
            cart_dict=self.get_cart_dict(user.id)
            skus=SKU.objects.filter(id__in=cart_dict.keys())
            sku_ids=[]
            for sku in skus:
                selected=int(cart_dict[sku.id]['selected'])
                if selected==0:
                    continue
                cart_count=int(cart_dict[sku.id]['count'])
                sku_ids.append(sku.id)
                if sku.stock<cart_count:
                    transaction.savepoint_rollback(sid)
                    sku_ids.remove(sku.id)
                    return JsonResponse({'code': 50103, 'errmsg': '商品[%d]库存不足' % sku.id})

                version_old=sku.version
                result=SKU.objects.filter(id=sku.id,version=version_old).update(stock=sku.stock-cart_count,sales=sku.sales+cart_count,version=version_old+1)
                if result==0:
                    transaction.savepoint_rollback(sid)
                    sku_ids.remove(sku.id)
                    return JsonResponse({'code': 50104, 'errmsg': '操作太快了,请稍后重试'})
                OrderGoods.objects.create(
                    order_id=order_id,
                    sku_id=sku.id,
                    count=cart_count,
                    price=sku.price
                )
                total_count+=cart_count
                total_amount+=sku.price*cart_count
            order.total_count=total_count
            order.total_amount=total_amount
            order.save()

            transaction.savepoint_commit(sid)

        self.delete_redis_order(sku_ids,user.id)
        sku_goods=OrderGoods.objects.filter(order=order_id)
        order_string=''
        pay_url='https://openapi.alipaydev.com/gateway.do?'+order_string
        data={
            'saller':'Beauty shop',
            'total_amount':order.total_amount+order.freight,
            'order_id':order_id,
            'pay_url':pay_url
        }
        return JsonResponse({"code": 200, "data": data})




