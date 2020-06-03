import hashlib
import json
import time


from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from user.models import UserProfile


def tokens(request):
    if not request.method=='POST':
        result={'code':101,'error':'pls use post'}
        return JsonResponse(result)
    json_str=request.body
    if not json_str:
        result={'code':102,'error':'pls give me json'}
        return JsonResponse(result)
    json_obj=json.loads(json_str)
    username=json_obj.get('username')
    password=json_obj.get('password')
    if not username:
        result={'code':103,'error':'pls give me username'}
    if not password:
        result={'code':104,'error':'pls give me password'}
    user=UserProfile.objects.filter(username=username)
    if not user:
        result = {'code': 105, 'error': 'username or password is wrong !! '}
        return JsonResponse(result)
    user=user[0]
    m=hashlib.md5()
    m.update(password.encode())
    if m.hexdigest()!=user.password:
        result = {'code': 106, 'error': 'username or password is wrong'}
        return JsonResponse(result)
    token=make_token(username)
    result = {'code': 200, 'username': username, 'data': {'token': token.decode()}}
    return JsonResponse(result)

def make_token(username, expire=3600 * 24):
    # 官方jwt / 自定义jwt
    import jwt
    key = '123456'
    now = time.time()
    payload = {'username': username, 'exp': int(now + expire)}
    return jwt.encode(payload, key, algorithm='HS256')