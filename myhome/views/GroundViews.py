from django.shortcuts import render

from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
from ..models import *
from ..middleware import JWTMiddleware
from ..utils.jsonSerialize import serialize_models
from ..utils.fileSystem import upload
import time



# 帖子列表
def searchType(request):
    data = request.GET.dict ()
    type = data.get("type",None)
    if type == "吐槽" or type == "咨询":
        data_list = Article.objects.filter(type=type).all()
    else:
        data_list = Article.objects.all()
    # 序列化数据集对象
    data_list = serialize_models(data_list)
    # 查询子项
    for item in data_list:
        obj1 = UserMsg.objects.filter(id=item['id']).first()
        item["user_info"] = serialize_models(obj1)
    return JsonResponse ({'msg': f'获取{type}发帖列表成功 ！', 'data': data_list, 'code': 200})

# 搜索帖子
def findKeywords(request):
    data = request.GET.dict ()
    keywords = data.get("keywords",None)
    data_list = Article.objects.filter(content__icontains=keywords).all()
    # 序列化数据集对象
    data_list = serialize_models(data_list)
    # 查询子项
    for item in data_list:
        obj1 = UserMsg.objects.filter(id=item['id']).first()
        item["user_info"] = serialize_models(obj1)
    return JsonResponse ({'msg': f'查询发帖列表成功 ！', 'data': data_list, 'code': 200})


# 他人主页
def otherAbout(request):
    data = request.GET.dict ()
    user_id = data.get("user_id",None)
    data_list = Article.objects.filter(user_id=user_id).all()
    # 序列化数据集对象
    data_list = serialize_models(data_list)
    # 查询子项
    for item in data_list:
        obj1 = UserMsg.objects.filter(id=item['id']).first()
        item["user_info"] = serialize_models(obj1)
    # 他人信息
    user_obj = UserMsg.objects.filter (id=user_id).first ()
    user_obj = serialize_models(user_obj)
    return_list = {
        "data_list":data_list,
        "user_info":user_obj
    }
    return JsonResponse ({'msg': f'查询发帖列表成功 ！', 'data': return_list, 'code': 200})

# 文章详情
def articleDetail(request):
    data = request.GET.dict ()
    article_id = data.get("article_id",None)
    data_detail = Article.objects.filter(id=article_id).first()
    data_detail = serialize_models(data_detail)
    # 发帖人信息
    user_id = data_detail.get("user_id",None)
    user_obj = UserMsg.objects.filter (id=user_id).first ()
    user_obj = serialize_models(user_obj)
    data_detail["user_info"] = user_obj
    # 其他人评论信息
    article_id = data_detail.get("id",None)
    comment_list = Comment.objects.filter (article_id=article_id).all ()
    comment_list = serialize_models(comment_list)
    for item in comment_list:
        user_obj = UserMsg.objects.filter (id=user_id).first ()
        item["user_info"] = serialize_models(user_obj)
    return_list = {
        "data_detail":data_detail,
        "comment_list":comment_list,
    }
    return JsonResponse ({'msg': f'获取帖子详情成功 ！', 'data': return_list, 'code': 200})
