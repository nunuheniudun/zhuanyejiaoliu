from django.shortcuts import render

from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
from ..models import *
from ..middleware import JWTMiddleware
from ..utils.jsonSerialize import serialize_models
from ..utils.fileSystem import upload
import time



# 创建帖子
def articleCreate(request):
    data = request.POST.dict()
    # 添加注册时间
    data['create_time'] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
    data['appri_count'] = 0
    data['collect_count'] = 0
    data['comment_count'] = 0
    # 获取请求头上的token,转换成user_id
    user_id = JWTMiddleware.get_parse_token(request)
    data['user_id'] = user_id
    # 接收上传的文件图片
    file = request.FILES.get ('file', None)
    if file:
        filename = upload(file)
        data['article_img_url'] = filename
        data.pop("file",None)
    Article(**data).save()
    return JsonResponse ({'msg': '发布帖子成功！！', 'code': 200})

# 更新帖子
def articleUpdate(request):
    data = request.POST.dict()
    # 添加注册时间
    data['create_time'] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
    data['appri_count'] = 0
    data['collect_count'] = 0
    data['comment_count'] = 0
    # 获取请求头上的token,转换成user_id
    user_id = JWTMiddleware.get_parse_token(request)
    data['user_id'] = user_id
    # 接收上传的文件图片
    file = request.FILES.get ('file', None)
    if file:
        filename = upload(file)
        data['article_img_url'] = filename
        data.pop("file",None)
    article_id = data.get("article_id",None)
    data.pop("article_id",None)
    obj = Article.objects.filter (id=article_id)
    if obj.exists():
        obj.update(**data)
    return JsonResponse ({'msg': '更新帖子成功！！', 'code': 200})

# 点赞帖子
def articleAppri(request):
    data = request.POST.dict()
    article_id = data.get("article_id",None)
    obj = Article.objects.filter (id=article_id)
    if obj.exists():
        obj.update(appri_count=obj.first().appri_count+1)
    return JsonResponse ({'msg': '点赞帖子成功！！', 'code': 200})

# 收藏帖子
def articleCollect(request):
    data = request.POST.dict()
    # 添加注册时间
    data = request.POST.dict()
    article_id = data.get("article_id",None)
    obj = Article.objects.filter (id=article_id)
    if obj.exists():
        obj.update(collect_count=obj.first().collect_count+1)
        # 获取请求头上的token,转换成user_id
        user_id = JWTMiddleware.get_parse_token (request)
        new_data = {
            "article_id":article_id,
            "user_id":user_id
        }
        Collection(**new_data).save()
    return JsonResponse ({'msg': '收藏帖子成功！！', 'code': 200})

# 浏览帖子
def articleView(request):
    data = request.POST.dict()
    article_id = data.get("article_id",None)
    # 获取请求头上的token,转换成user_id
    user_id = JWTMiddleware.get_parse_token (request)
    new_data = {
        "article_id": article_id,
        "user_id": user_id
    }
    VewHistory (**new_data).save ()
    return JsonResponse ({'msg': '浏览帖子成功！！', 'code': 200})

# 评论帖子
def articleComment(request):
    data = request.POST.dict()
    article_id = data.get("article_id",None)
    obj = Article.objects.filter (id=article_id)
    if obj.exists():
        obj.update(comment_count=obj.first().comment_count+1)
        # 获取请求头上的token,转换成user_id
        user_id = JWTMiddleware.get_parse_token (request)
        new_data = {
            "article_id":article_id,
            "user_id":user_id,
            "content":data.get("content",None),
            "create_time": time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
        }
        Comment(**new_data).save()
    return JsonResponse ({'msg': '评论帖子成功！！', 'code': 200})
