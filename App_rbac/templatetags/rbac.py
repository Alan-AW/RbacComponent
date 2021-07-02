from django.template import Library
from django.conf import settings as SYS

register = Library()

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
    return {
        'menuDict': menuDict
    }

