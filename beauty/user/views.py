import base64
import hashlib
import json
import random

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic import View
from django_redis import get_redis_connection

from beauty import settings
from celery_tasks.user_tasks import send_verify
from utils.loging_decorator import logging_check
from .models import UserProfile,Address


class BaseUserView(View):
    def check_args(self,data,length):
        if len(data)!=length:
            raise
        for key,value in data.items():
            if not value:
                raise
        return data

class Users(BaseUserView):
    def post(self,request):
        # print(request.body)
        # b'{"uname":"111","password":"111","phone":"13091463622","email":"dada@tedu.cn"}'
        json_obj=json.loads(request.body)
        # print(json_obj)
        # {'uname': '111', 'password': '111', 'phone': '13091463622', 'email': 'dada@tedu.cn'}
        data=self.check_args(json_obj,4)
        # print(data)
        # {'uname': '111', 'password': '111', 'phone': '13091463622', 'email': 'dada@tedu.cn'}
        username=data.get('uname')
        password=data.get('password')
        email=data.get('email')
        phone=data.get('phone')

        old_user=UserProfile.objects.filter(username=username)
        if old_user:
            result={'code':206,'error':'Your username is already used'}
            return JsonResponse(result)

        m=hashlib.md5()
        m.update(password.encode())
        try:
            UserProfile.objects.create(username=username,password=m.hexdigest(),email=email,phone=phone)
        except:
            result={'code':208,'error':'server is busy'}
            return JsonResponse(result)

        try:
            code='%d'%random.randint(1000,9999)
            code_str=code+'/'+username
            active_code=base64.urlsafe_b64encode(code_str.encode(encoding='utf-8')).decode('utf-8')
            redis_conn=get_redis_connection('verify_email')
            redis_conn.set('email_active_%s'%username,active_code)
            # http://127.0.0.1:7000/dadashop/templates/active.html?code=MjAyNi8xMTc=
            verify_url=settings.ACTIVE_HOST+'/templates/active.html?code=%s'%(active_code)
            token=make_token(username)
            send_verify.delay(email=email,verify_url=verify_url,sendtype=1)
        except Exception as e:
            result={'code':10111,'error':'something bad'}
            return JsonResponse(result)
        result={'code':200,'username':username,'token':token.decode()}
        return JsonResponse(result)

def make_token(username,expire=3600*24):
    import jwt,time
    key='123456'
    now=time.time()
    payload={'username':username,'exp':int(now+expire)}
    token=jwt.encode(payload,key,algorithm='HS256')
    return token

class ActiveView(View):
    def get(self,request):
        code=request.GET.get('code',None)
        if not code:
            return JsonResponse({'code':10113,'error':'Error activating link parameters'})
        verify_code=base64.urlsafe_b64decode(code.encode('utf-8')).decode()
        random_code,username=verify_code.split('/')
        redis_conn=get_redis_connection('verify_email')
        result=redis_conn.get('email_active_%s'%username).decode()
        print(result)
        if not result:
            return JsonResponse({'code':10112,'error':'Link is invalid and resend it!'})
        if code!=result:
            return JsonResponse({'code': 10112, 'error': 'Link is invalid and resend it!'})
        try:
            user=UserProfile.objects.get(username=username)
        except Exception as e:
            return JsonResponse({'code': 10122, 'error': 'User query error'})
        user.isActive=True
        user.save()
        redis_conn.delete('email_active_%s'%username)
        return JsonResponse({'code':200,'data':'ok'})

class AddressView(BaseUserView):
    @logging_check
    def get(self,request,username):
        user=request.user
        try:
            all_address=Address.objects.filter(uid=user.id,isActive=True)
        except Exception as e:
            return JsonResponse({'code': 10114, 'error': 'Error in Address Query!'})
        addresslist=[]
        for value in all_address:
            each_address={}
            each_address['id']=value.id
            each_address['address']=value.address
            each_address['receiver']=value.receiver
            each_address['receiver_mobile'] = value.receiver_mobile
            each_address['tag'] = value.tag
            each_address['is_default'] = value.default_address
            addresslist.append(each_address)
        return JsonResponse({'code': 200, 'addresslist': addresslist})


    @logging_check
    def post(self,request,username):
        json_obj = json.loads(request.body)
        data = self.check_args(json_obj, 5)
        receiver = data.get('receiver')
        address = data.get('address')
        receiver_phone = data.get('receiver_phone')
        postcode = data.get('postcode')
        tag = data.get('tag')
        user=request.user

        query_address=Address.objects.filter(uid=user.id)
        default_status=False
        if not query_address:
            default_status=True
        try:
            Address.objects.create(
                uid=user,
                receiver=receiver,
                address=address,
                default_address=default_status,
                receiver_mobile=receiver_phone,
                isActive=True,
                postcode=postcode,
                tag=tag,
            )
        except Exception as e:
            return JsonResponse({'code': 10120, 'error': 'Address storage exception'})
        return JsonResponse({'code': 200, 'data': '新增地址成功！'})
    @logging_check
    def delete(self,request,username,id):
        print('id',id)
        if not id:
            return JsonResponse({'code': 10122, 'error': 'Get address id error'})
        try:
            address=Address.objects.get(id=id)
        except Address.DoesNotExist as e:
            # 此刻应该写个日志
            return JsonResponse({'code': 10121, 'error': 'Get address exception'})
        try:
            address.isActive=False
            address.save()
        except Exception as e:
            return JsonResponse({'code': 10122, 'error': 'delete address error'})
        return JsonResponse({'code': 200, 'data': '删除地址成功！'})

    @logging_check
    def put(self,request,username,id):
        if not id:
            return JsonResponse({'code': 10122, 'error': 'Get address id error'})
        json_obj = json.loads(request.body)
        data = self.check_args(json_obj, 5)
        address = data.get('address')
        receiver = data.get('receiver')
        tag = data.get('tag')
        receiver_mobile = data.get('receiver_mobile')
        data_id = data.get('id')
        if int(id) != data_id:
            return JsonResponse({'code': 12345, 'error': 'ID error'})
        try:
            filter_address=Address.objects.get(id=id)
        except Exception as e:
            return JsonResponse({'code': 10122, 'error': 'Get address exception!'})
        try:
            filter_address.receiver = receiver
            filter_address.receiver_mobile = receiver_mobile
            filter_address.address = address
            filter_address.tag = tag
            filter_address.save()
        except Exception as e:
            return JsonResponse({'code': 10123, 'error': '修改地址失败！'})
        return JsonResponse({'code': 200, 'data': '修改地址成功！'})

class DefaultAddressView(BaseUserView):
    """
    用来修改默认地址
    """
    @logging_check
    def post(self, request, username):
        """
        用来修改默认地址
        :param address_id:用户修改地址的id
        """
        # 先根据address_id 来匹配出用户的id
        json_obj = json.loads(request.body)
        print('request.body',request.body)
        data = self.check_args(json_obj,1)
        address_id = data.get('id')
        # 需要将此条地址设为默认地址，其他的需要设置为非默认地址。
        user = request.user
        user_address = Address.objects.filter(uid=user.id, isActive=True)
        for single_address in user_address:
            if single_address.id == address_id:
                single_address.default_address = True
                single_address.save()
            else:
                single_address.default_address = False
                single_address.save()
        return JsonResponse({'code':200,'data':'设为默认成功！'})




