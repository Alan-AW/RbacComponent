from django.urls import path, re_path, include
from App_rbac.views import role  # 角色
from App_rbac.views import user

app_name = 'App_rbac'
urlpatterns = [
    # 角色管理
    path('role/list/', role.RoleList.as_view(), name='role_list'),
    path('role/add/', role.RoleAdd.as_view(), name='role_add'),
    re_path(r'role/edit/(?P<pk>\d+)/$', role.RoleEdit.as_view(), name='role_edit'),
    re_path(r'role/del/(?P<pk>\d+)/$', role.RoleDel.as_view(), name='role_del'),
    # 用户管理
    path('user/list/', user.UserList.as_view(), name='user_list'),
    path('user/add/', user.UserAdd.as_view(), name='user_add'),
    # path('user/add/', user.user_add, name='user_add'),
    re_path(r'user/edit/(?P<pk>\d+)/$', user.UserEdit.as_view(), name='user_edit'),
    re_path(r'user/del/(?P<pk>\d+)/$', user.UserDel.as_view(), name='user_del'),

]
