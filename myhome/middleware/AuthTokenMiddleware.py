import re
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from . import JWTMiddleware             # 引入jwt中间件
from ..models import *

# 对请求进行拦截
class AuthTokenMiddleware(MiddlewareMixin):
  def process_request(self, request):
    # 允许自由访问的路由
    allow = [
      '/',
      '/api/admin/login',
      '/api/admin/register',
    ]
    # 检验路由，和session
    route = request.path
    # 先检测是否是允许访问的路由
    haveAuth = False
    for item in allow:
      if route == item:
        haveAuth = True
    # 再检测有效性，和存在性
    if not haveAuth:
      # 获取请求头上的token
      str_token = request.META.get ('HTTP_TOKEN',None)
      user_obj = JWTMiddleware.parse_jwt(str_token)
      if not user_obj:
        # 检测token有效性失败
        return JsonResponse({'msg':'当前没有权限进入！请输入有效token','code':403})
      else:
        # 再检测存在性
        token_obj = UserMsg.objects.filter (token=str_token,is_delete='0').first ()
        if not token_obj:
          # 检测token存在性失败
          return JsonResponse({'msg':'当前帐号没有登录，请进行登录！','code':403})

