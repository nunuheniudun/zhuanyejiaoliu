from django.urls import path,re_path
from ..views import *

urlpatterns = [
    # 测试接口
    path('',IndexViews.test,name="myhome_test"),

    # 认证API
    path('api/admin/login',IndexViews.login,name="myhome_login"),
    path('api/admin/register',IndexViews.register,name="myhome_register"),
    path('api/admin/logout',IndexViews.logout,name="myhome_logout"),
    path('api/admin/unregister',IndexViews.unregister,name="myhome_unregister"),

    # 前台API
    path('api/home/user/about',UserViews.about,name="myhome_about"),
    path ('api/home/user/update', UserViews.update,name="myhome_update"),
    path ('api/home/user/password', UserViews.password,name="myhome_password"),
    path ('api/home/user/username', UserViews.updateUsername,name="myhome_username"),
    path ('api/home/user/avatar', UserViews.updateAvatar,name="myhome_avatar"),

    # 广场功能
    path ('api/home/ground/search', GroundViews.searchType, name="myhome_searchType"),
    path ('api/home/ground/find', GroundViews.findKeywords, name="myhome_findKeywords"),
    path ('api/home/ground/other_about', GroundViews.otherAbout, name="myhome_otherAbout"),
    path ('api/home/ground/article_detail', GroundViews.articleDetail, name="myhome_articleDetail"),

    # 帖子信息
    path ('api/home/article/create', ArticleViews.articleCreate, name="myhome_articleCreate"),
    path ('api/home/article/update', ArticleViews.articleUpdate, name="myhome_articleUpdate"),

    path ('api/home/article/appri', ArticleViews.articleAppri, name="myhome_articleAppri"),
    path ('api/home/article/collect', ArticleViews.articleCollect, name="myhome_articleAppri"),
    path ('api/home/article/view', ArticleViews.articleView, name="myhome_articleAppri"),
    path ('api/home/article/comment', ArticleViews.articleComment, name="myhome_articleComment"),

    # 用户信息
    path('api/home/user/collect_list',UserViews.collect_list,name="myhome_collect_list"),
    path('api/home/user/article_list',UserViews.article_list,name="myhome_collect_list"),
    path('api/home/user/comment_list',UserViews.comment_list,name="myhome_collect_list"),
    path('api/home/user/view_list',UserViews.view_list,name="myhome_view_list"),



    # 后台API（略）
    path ('api/admin/searchAll', AdminViews.searchAll,name="myhome_searchAll"),
    path ('api/admin/searchDelAll', AdminViews.searchDelAll,name="myhome_searchDelAll"),
    path ('api/admin/searchUseAll', AdminViews.searchUseAll,name="myhome_searchUseAll"),
    path ('api/admin/search', AdminViews.search,name="myhome_search"),

]
'''



'''
