from django.shortcuts import render

from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse, HttpResponse
from ..models import *
from ..middleware import JWTMiddleware
from ..utils.jsonSerialize import serialize_models
import time


# 查询所有用户
def searchAll(request):
    data_list = UserMsg.objects.all()
    data_list = serialize_models(data_list)
    return JsonResponse ({'msg': '获取所有用户信息成功！','data':data_list, 'code': 200})


# 查询注销用户
def searchDelAll(request):
    data_list = UserMsg.objects.filter(is_delete='1')
    data_list = serialize_models(data_list)
    return JsonResponse ({'msg': '获取所有注销用户信息成功！','data':data_list, 'code': 200})


# 查询非注销用户
def searchUseAll(request):
    data_list = UserMsg.objects.filter(is_delete='0')
    data_list = serialize_models(data_list)
    return JsonResponse ({'msg': '获取所有非注销用户信息成功！','data':data_list, 'code': 200})


# 查询用户(昵称)
def search(request):
    data = request.GET.dict ()
    data_list = UserMsg.objects.filter(username__icontains=data['username'])
    data_list = serialize_models(data_list)
    return JsonResponse ({'msg': '查询用户信息成功！','data':data_list, 'code': 200})
