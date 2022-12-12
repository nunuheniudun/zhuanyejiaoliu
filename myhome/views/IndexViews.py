from django.shortcuts import render

from django.contrib.auth.hashers import make_password,check_password
from django.http import JsonResponse,HttpResponse
from ..models import *
from ..middleware import JWTMiddleware
import time


# 测试接口
def test(request):
    return HttpResponse("成功访问django接口")

# 登录帐号
def login(request):
    data = request.POST.dict()
    data.pop("csrfmiddlewaretoken",None)
    # 先检测学生表
    user_obj = UserMsg.objects.filter(username=data['username'])
    user_obj_filter = user_obj.first()
    if not user_obj_filter:
        return JsonResponse ({'msg': '登录失败！帐号不存在！', 'code': 403})
    else:
        # 检测密码是否正确
        res = check_password (data['password'], user_obj_filter.password)
        if not res:
            return JsonResponse ({'msg': '登录失败！密码错误！', 'code': 403})
        else:
            # 生成token身份认证, 并存储在数据库
            token = JWTMiddleware.make_jwt(user_obj_filter.id)
            user_obj.update(token=token)
            return JsonResponse ({'msg': '登录成功！','token':token, 'code': 200})

# 注册帐号
def register(request):
    data = request.POST.dict()
    # 添加注册时间
    data['register_time'] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
    data['is_delete'] = '0'
    # 密码加密
    data['password'] = make_password (data['password'], None, 'pbkdf2_sha256')

    # 查询是否帐号已经被注册
    obj = UserMsg.objects.filter(username=data['username']).first()
    if not obj:
        UserMsg(**data).save()
        return JsonResponse ({'msg': '注册成功！', 'code': 200})
    else:
        return JsonResponse ({'msg': '当前用户昵称已经被注册，请重新输入！', 'code': 403})

## 退出登录
def logout(request):
    # 获取请求头上的token,转换成user_id
    user_id = JWTMiddleware.get_parse_token(request)
    user_obj = UserMsg.objects.filter(id=user_id)
    user_obj.update(token="")
    return JsonResponse ({'msg': '退出登录成功！', 'code': 200})

## 注销帐号
def unregister(request):
    # 获取请求头上的token,转换成user_id
    user_id = JWTMiddleware.get_parse_token(request)
    user_obj = UserMsg.objects.filter(id=user_id)
    # 添加注册时间
    data = {
        'token':'',
        'delete_time':time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()),
        'is_delete':'1'
    }
    user_obj.update(**data)
    return JsonResponse ({'msg': '注销帐号成功！', 'code': 200})