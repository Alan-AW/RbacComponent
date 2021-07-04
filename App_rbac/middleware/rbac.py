from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render, redirect, HttpResponse
from django.conf import settings as SYS
import re


class RbacMiddleware(MiddlewareMixin):
    '''
    用户权限信息的校验
    '''

    def process_request(self, request):
        '''
        当用户请求刚进入时做这个校验
        1.获取当前用户请求的url
        2.去session中获取保存的当前用户的所有权限url列表，
        3.权限信息的匹配：只要有一个能匹配成功即可
        '''
        # request.path_info  会获取到当前用户访问的url  与携带的参数无关

        # ******进行白名单设置
        current_url = request.path_info
        for valid in SYS.VALID_URL:
            if re.match(valid, current_url):
                # 直接通过白名单校验，否则才走下面的权限验证
                return None  # 中间件不拦截，直接去视图函数，有返回值便会被拦截
        permissionList = request.session.get(SYS.PERMISSION_SESSION_KEY)
        if not permissionList:
            return HttpResponse('请先登录！！')
        flag = False

        urlRecord = [
            {'title': '首页', 'url': '#'}
        ]

        for item in permissionList:
            reg = '^%s$' % item['url']
            if re.match(reg, current_url):
                flag = True
                # 自动判断，如果pid为true（有值，存在值即为true），则保存了pid，否则保存了id
                request.currentSelectedPermission = item['pid'] or item['id']
                if not item['pid']:
                    urlRecord.extend([{'title': item['title'], 'url': item['url'], 'class': 'active'}])
                else:
                    urlRecord.extend([
                        {'title': item['p_title'], 'url': item['p_url']},
                        {'title': item['title'], 'url': item['url'], 'class': 'active'},
                    ])
                print(urlRecord)
                request.breadcrumb = urlRecord
                break
        if not flag:
            return HttpResponse('无权访问!!')

'''
 方案一：
     if url == current_url:
         return '拥有权限'
     问题一：
         session中存的是一级url地址（/user/list/）,如果用户访问的是（/user/list/<?P(\d+)>）
         就会匹配不成功
 方案二：
     使用正则进行匹配：
     r = re.match(url, current_url)
     if r:  # 拥有权限？？
         pass
     问题二：
         基于问题一正则可以匹配上包含正确路由的地址，但是在二级路由输入所有符合正则的内容，这个地址任然会匹配成功
 方案三：
     将session中保存的权限路由加上起始终止符：reg = '^%S$' % url
 '''
