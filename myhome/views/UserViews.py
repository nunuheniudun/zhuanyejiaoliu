from django.shortcuts import render

from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
from ..models import *
from ..middleware import JWTMiddleware
from ..utils.jsonSerialize import serialize_models
from ..utils.fileSystem import upload
import time



# 一、个人信息
# 用户详情
def about(request):
    # 获取请求头上的token,转换成user_id
    user_id = JWTMiddleware.get_parse_token(request)
    user_obj = UserMsg.objects.filter(id=user_id).first()
    # 序列化数据集对象
    user_obj = serialize_models(user_obj)
    return JsonResponse ({'msg': '获取个人信息成功 ！', 'data': user_obj, 'code': 200})


# 修改信息
def update(request):
    data = request.POST.dict ()
    # 添加修改时间
    data['update_time'] = time.strftime ('%Y-%m-%d %H:%M:%S', time.localtime ())
    data['is_delete'] = '0'
    # 获取请求头上的token,转换成user_id
    user_id = JWTMiddleware.get_parse_token(request)
    user_obj = UserMsg.objects.filter (id=user_id)
    user_obj.update(**data)
    return JsonResponse ({'msg': '更新用户信息成功！', 'code': 200})

# 修改用户名
def updateUsername(request):
    data = request.POST.dict ()
    # 添加修改时间
    data['update_time'] = time.strftime ('%Y-%m-%d %H:%M:%S', time.localtime ())
    data['is_delete'] = '0'
    # 获取请求头上的token,转换成user_id
    user_id = JWTMiddleware.get_parse_token(request)
    # 如果当前用户名没有被使用，就更新数据
    username = data.get("username",None)
    pre_user_obj = UserMsg.objects.filter( Q(username=username) & ~Q(id=user_id))
    if pre_user_obj.exists():
        return JsonResponse ({'msg': '当前昵称已经被使用！', 'code': 403})
    else:
        user_obj = UserMsg.objects.filter (id=user_id)
        user_obj.update(**data)
        return JsonResponse ({'msg': '更新用户信息成功！', 'code': 200})


# 修改头像
def updateAvatar(request):
    data = request.POST.dict ()
    # 添加修改时间
    data['update_time'] = time.strftime ('%Y-%m-%d %H:%M:%S', time.localtime ())
    data['is_delete'] = '0'
    # 接收上传的文件
    file = request.FILES.get ('file', None)
    filename = upload(file)
    # 保存图图片
    # 获取请求头上的token,转换成user_id
    user_id = JWTMiddleware.get_parse_token(request)
    user_obj = UserMsg.objects.filter (id=user_id)
    user_obj.update(avatar_url=filename)
    return JsonResponse ({'msg': '更新用户头像成功！', 'code': 200})


# 修改密码
def password(request):
    data = request.POST.dict ()
    # 添加修改时间
    data['update_time'] = time.strftime ('%Y-%m-%d %H:%M:%S', time.localtime ())
    data['is_delete'] = '0'
    # 获取请求头上的token,转换成user_id
    user_id = JWTMiddleware.get_parse_token(request)
    user_obj = UserMsg.objects.filter (id=user_id)
    user_obj_filter = UserMsg.objects.filter (id=user_id).first()

    # 检测旧密码是否相同
    res = check_password (data['old_password'], user_obj_filter.password)
    if not res:
        return JsonResponse ({'msg': '输入的旧密码错误！请重新输入！', 'code': 403})
    else:
        # 加密新密码
        data['password'] = make_password (data['new_password'], None, 'pbkdf2_sha256')
        del data['old_password']
        del data['new_password']
        user_obj.update(**data)
        return JsonResponse ({'msg': '更新登录密码成功！', 'code': 200})


# 二、用户信息
# 收藏列表
def collect_list(request):
    # 获取请求头上的token,转换成user_id
    user_id = JWTMiddleware.get_parse_token(request)
    data_list = Collection.objects.filter(user_id=user_id).all()
    # 序列化数据集对象
    data_list = serialize_models(data_list)
    # 查询子项
    for item in data_list:
        obj1 = UserMsg.objects.filter(id=item['id']).first()
        item["user_info"] = serialize_models(obj1)
        obj2 = Article.objects.filter(id=item['id']).first()
        item["article_info"] = serialize_models(obj2)
    return JsonResponse ({'msg': '获取收藏列表成功 ！', 'data': data_list, 'code': 200})

# 评论列表
def comment_list(request):
    # 获取请求头上的token,转换成user_id
    user_id = JWTMiddleware.get_parse_token(request)
    data_list = Comment.objects.filter(user_id=user_id).all()
    # 序列化数据集对象
    data_list = serialize_models(data_list)
    # 查询子项
    for item in data_list:
        obj1 = UserMsg.objects.filter(id=item['id']).first()
        item["user_info"] = serialize_models(obj1)
        obj2 = Article.objects.filter(id=item['id']).first()
        item["article_info"] = serialize_models(obj2)
    return JsonResponse ({'msg': '获取评论列表成功 ！', 'data': data_list, 'code': 200})

# 发帖列表
def article_list(request):
    # 获取请求头上的token,转换成user_id
    user_id = JWTMiddleware.get_parse_token(request)
    data_list = Article.objects.filter(user_id=user_id).all()
    # 序列化数据集对象
    data_list = serialize_models(data_list)
    # 查询子项
    for item in data_list:
        obj1 = UserMsg.objects.filter(id=item['id']).first()
        item["user_info"] = serialize_models(obj1)
    return JsonResponse ({'msg': '获取发帖列表成功 ！', 'data': data_list, 'code': 200})

# 浏览列表
def view_list(request):
    # 获取请求头上的token,转换成user_id
    user_id = JWTMiddleware.get_parse_token(request)
    data_list = VewHistory.objects.filter(user_id=user_id).all()
    # 序列化数据集对象
    data_list = serialize_models(data_list)
    # 查询子项
    for item in data_list:
        obj2 = Article.objects.filter(id=item['article_id']).first()
        item["article_info"] = serialize_models(obj2)
    return JsonResponse ({'msg': '获取浏览历史列表成功 ！', 'data': data_list, 'code': 200})
