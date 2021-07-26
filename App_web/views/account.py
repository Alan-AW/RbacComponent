from django.shortcuts import render, redirect, HttpResponse
from django.views import View

from App_rbac.models import *  # 用户表的引入应该在当前App内
from App_rbac.service.initPermission import initPermission  # 用户权限初始化


class Login(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        user = request.POST.get('user')
        pwd = request.POST.get('password')
        userObj = UserInfo.objects.filter(name=user, password=pwd).first()
        if not userObj:
            return render(request, 'login.html', {'msg': '用户名或密码错误'})
        # 2.用户权限初始化
        initPermission(userObj, request)  # 权限系统的封装
        return redirect('/customer/list/')


def logout(request):
    if request.method == 'GET':
        return redirect(request, '/login/')
