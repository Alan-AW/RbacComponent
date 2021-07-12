from django.views import View
from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from App_rbac.models import Menu, Permission
from App_rbac.service.urls import memoryReverse
from App_rbac.forms.menu import MenuModelForm, SecondMenuModelForm, PermissionModelForm

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

        # 在没有选中一级菜单的情况下是否展示新增按钮：
        menu_exists = Menu.objects.filter(id=menuId).exists()
        if not menu_exists:
            menuId = None

        if menuId:
            secondMenus = Permission.objects.filter(menu_id=menuId)  # 根据选择的一级菜单获取倒二级菜单
        else:
            secondMenus = []

        # 在没有选中二级菜单的情况下是否展示新增按钮：
        second_menu_exists = Permission.objects.filter(id=secondMenuId).exists()
        if not second_menu_exists:
            secondMenuId = None
        if secondMenuId:
            permissions = Permission.objects.filter(pid=secondMenuId)  # 根据选择的二级菜单查询到对应的所有权限
        else:
            permissions = []

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


"""
权限管理
"""


class PermissionAdd(View):
    def get(self, request, secondMenuId):
        # menuObj = Menu.objects.filter(id=menuId).first()
        form = PermissionModelForm()
        return render(request, 'rbac/change.html', locals())

    def post(self, request, secondMenuId):
        form = PermissionModelForm(data=request.POST)
        if form.is_valid():
            secondMenuObj = Permission.objects.filter(id=secondMenuId).first()
            if not secondMenuObj:
                return HttpResponse('当前二级菜单不存在，请重新选择二级菜单！')
            # form.instance中：包含了用户提交的所有值
            form.instance.pid = secondMenuObj
            """
             ↑ 这句话相当于执行了三次操作
            - instance = Permission(title='用户输入值', url='用户输入', name='用户输入')
            - instance.pid = secondMenuObj
            - instance.save()
            form.save()
            其实就是保存数据倒数据库中， 表单收集倒的用户输入的数据已经被实例化为了一个对象 ————> instance
            """
            form.save()
            url = memoryReverse(request, 'rbac:menu_list')
            return redirect(url)
        else:
            return render(request, 'rbac/change.html', locals())


def permission_edit(request, pk):
    permissionObj = Permission.objects.filter(id=pk).first()
    if request.method == 'GET':
        form = PermissionModelForm(instance=permissionObj)
        return render(request, 'rbac/change.html', locals())
    form = PermissionModelForm(data=request.POST, instance=permissionObj)
    if form.is_valid():
        form.save()
        return redirect(memoryReverse(request, 'rbac:menu_list'))
    return render(request, 'rbac/change.html', locals())


def permission_del(request, pk):
    url = memoryReverse(request, 'rbac:menu_list')
    if request.method == 'GET':
        return render(request, 'rbac/delete.html', {'cancelUrl': url})
    Permission.objects.filter(id=pk).delete()
    return redirect(url)
