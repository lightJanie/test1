
import jwt
from django.http import JsonResponse
import json

from user.models import UserProfile

TOKEN_KEY='123456'
def logging_check(func):
    def wrapper(self,request,*args,**kwargs):
        token=request.META.get('HTTP_AUTHORIZATION')
        if not token:
            result={'code':403,'error':'pls login'}
            return JsonResponse(result)
        try:
            res=jwt.decode(token,TOKEN_KEY)
        except Exception as e:
            print('jwt decode error is %s'%e)
            result={'code':403,'error':'pls login'}
            return JsonResponse(result)
        except jwt.ExpiredSignatureError:
            result={'code':403,'error':'pls login'}
            return JsonResponse(result)

        username=res['username']
        user=UserProfile.objects.get(username=username)
        if not user:
            result={'code':208,'error':'user is not existed'}
            return JsonResponse(result)
        request.user=user
        return func(self,request,*args,**kwargs)
    return wrapper
