from django.views import View
from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from App_rbac.models import Menu, Permission
from App_rbac.service.urls import memoryReverse
from App_rbac.forms.menu import MenuModelForm, SecondMenuModelForm

"""
一级菜单管理
"""


class MenuList(View):
    """
    所有菜单
    """

    def get(self, request):
        menu = Menu.objects.all()
        menuId = request.GET.get('mid')  # 用户选择的一级菜单
        secondMenuId = request.GET.get('sid')  # 用户选择的二级菜单

        # get方法拿到的mid是字符串类型，前端页面做判断的时候从数据库中取出的id是整型
        if menuId:
            secondMenus = Permission.objects.filter(menu_id=menuId)  # 根据选择的一级菜单获取倒二级菜单
        else:
            secondMenus = []

        return render(request, 'rbac/menu_list.html', locals())

    def post(self, request):
        pass


class MenuAdd(View):
    """
    添加一级菜单
    """

    def get(self, request):
        form = MenuModelForm
        return render(request, 'rbac/change.html', locals())

    def post(self, request):
        form = MenuModelForm(data=request.POST)
        if form.is_valid():
            form.save()
            url = memoryReverse(request, 'rbac:menu_list')
            return redirect(url)
        else:
            return render(request, 'rbac/change.html', locals())


class MenuEdit(View):
    """
    菜单修改
    """

    def get(self, request, pk):
        menuObj = Menu.objects.filter(id=pk).first()
        if not menuObj:
            return HttpResponse('禁止操作!')  # 角色不存在
        form = MenuModelForm(instance=menuObj)
        return render(request, 'rbac/change.html', locals())

    def post(self, request, pk):
        menuObj = Menu.objects.filter(id=pk).first()
        form = MenuModelForm(instance=menuObj, data=request.POST)
        if form.is_valid():
            form.save()
            url = memoryReverse(request, 'rbac:menu_list')
            return redirect(url)


class MenuDel(View):
    """
    菜单删除
    """

    def get(self, request, pk):
        url = memoryReverse(request, 'rbac:menu_list')
        return render(request, 'rbac/delete.html', {'cancelUrl': url})

    def post(self, request, pk):
        Menu.objects.filter(id=pk).delete()  # 删除
        # 拼接出原搜索条件url，进行跳转
        url = memoryReverse(request, 'rbac:menu_list')
        return redirect(url)


"""
二级菜单管理
"""


class SecondMenuAdd(View):

    def get(self, request, menuId):
        """
        二级菜单的添加
        :param request:
        :param menuId: 默认的一级菜单ID(用于设置默认值)
        :return:
        """
        menuObj = Menu.objects.filter(id=menuId).first()
        form = SecondMenuModelForm(initial={'menu': menuObj})
        return render(request, 'rbac/change.html', locals())

    def post(self, request, menuId):
        form = SecondMenuModelForm(data=request.POST)
        if form.is_valid():
            form.save()
            url = memoryReverse(request, 'rbac:menu_list')
            return redirect(url)
        else:
            return render(request, 'rbac/change.html', locals())


def second_menu_edit(request, pk):
    permissionObj = Permission.objects.filter(id=pk).first()
    if request.method == 'GET':
        form = SecondMenuModelForm(instance=permissionObj)
        return render(request, 'rbac/change.html', locals())

    form = SecondMenuModelForm(data=request.POST, instance=permissionObj)
    if form.is_valid():
        form.save()
        return redirect(memoryReverse(request, 'rbac:menu_list'))
    return render(request, 'rbac/change.html', locals())


def second_menu_del(request, pk):
    url = memoryReverse(request, 'rbac:menu_list')
    if request.method == 'GET':
        return render(request, 'rbac/delete.html', {'cancelUrl': url})

    Permission.objects.filter(id=pk).delete()
    return redirect(url)
