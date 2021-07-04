from django.template import Library
from django.conf import settings as SYS
import re
from collections import OrderedDict

register = Library()  # 注册该组件


###################### 一级菜单和二级菜单只能选一个 #############################

# 一级菜单
# @register.inclusion_tag('rbac/staticMenu.html')
# def staticMenu(request):
#     menuList = request.session[SYS.MENU_SESSION_KEY]
#     return {
#         'menuList': menuList
#     }

# 二级菜单
@register.inclusion_tag('rbac/multiMenu.html')
def multiMenu(request):
    menuDict = request.session[SYS.MENU_SESSION_KEY]
    keyLIst = sorted(menuDict)  # 对字典的key进行排序
    orderedDict = OrderedDict()  # 创建了一个空的有序字典
    for key in keyLIst:
        val = menuDict[key]
        val['class'] = 'hide'  # 默认加了一个hide属性使其隐藏
        for per in val['children']:
            if per['id'] == request.currentSelectedPermission:
                per['class'] = 'active'
                val['class'] = ''
        orderedDict[key] = val

    return {
        'menuDict': orderedDict
    }

# 路径导航
@register.inclusion_tag('rbac/breadcrumb.html')
def breadcrumb(request):
    return {'recordList': request.breadcrumb}


