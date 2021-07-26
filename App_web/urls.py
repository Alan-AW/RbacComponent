from django.conf.urls import url
from App_web.views import customer
from App_web.views import payment
from App_web.views import account

app_name = 'App_web'
urlpatterns = [

    # 客户
    url(r'^customer/list/$', customer.customer_list, name='customer_list'),
    url(r'^customer/add/$', customer.customer_add, name='customer_add'),
    url(r'^customer/edit/(?P<cid>\d+)/$', customer.customer_edit, name='customer_edit'),
    url(r'^customer/del/(?P<cid>\d+)/$', customer.customer_del, name='customer_del'),
    # 数据批量导入&模版下载
    url(r'^customer/import/$', customer.customer_import, name='customer_import'),
    url(r'^customer/tpl/$', customer.customer_tpl, name='customer_tpl'),
    # 账单
    url(r'^payment/list/$', payment.payment_list, name='payment_list'),
    url(r'^payment/add/$', payment.payment_add, name='payment_add'),
    url(r'^payment/edit/(?P<pid>\d+)/$', payment.payment_edit, name='payment_edit'),
    url(r'^payment/del/(?P<pid>\d+)/$', payment.payment_del, name='payment_del'),
    # 用户登陆&退出
    url(r'^login/$', account.Login.as_view(), name='login'),
    url(r'^logout/$', account.logout, name='logout')

]
