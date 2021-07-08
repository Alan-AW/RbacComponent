from django.views import View
from django.urls import reverse
from django.shortcuts import render, redirect, HttpResponse
from App_rbac.models import UserInfo
from App_rbac.forms.user import UserModelForm, UpdateUserModelForm

"""
    用户管理
"""


class UserList(View):
    def get(self, request):
        userQuerySet = UserInfo.objects.all()
        return render(request, 'rbac/user_list.html', locals())


class UserAdd(View):
    def get(self, request):
        form = UserModelForm()
        return render(request, 'rbac/change.html', locals())

    def post(self, request):
        form = UserModelForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('rbac:user_list'))
        else:
            return render(request, 'rbac/change.html', locals())


class UserEdit(View):
    def get(self, request, pk):
        userObj = UserInfo.objects.filter(id=pk).first()
        if not userObj:
            return HttpResponse('该用户不存在!')
        form = UpdateUserModelForm(instance=userObj)
        return render(request, 'rbac/change.html', locals())

    def post(self, request, pk):
        form = UpdateUserModelForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('rbac:user_list'))
        else:
            return render(request, 'rbac/change.html', locals())


class UserDel(View):
    pass
