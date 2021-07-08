from django.views import View
from django.shortcuts import render, redirect, HttpResponse
from App_rbac.models import UserInfo



"""
    用户管理
"""


class UserList(View):
    def get(self, request):
        userQuerySet = UserInfo.objects.all()
        return render(request, 'rbac/user_list.html', locals())


class UserAdd(View):
    pass


class UserEdit(View):
    pass


class UserDel(View):
    pass

