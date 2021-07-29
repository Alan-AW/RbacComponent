from django.db import models
from App_rbac.models import UserInfo as RbacUserInfo


class UserInfo(RbacUserInfo):
    """
    用户表
    """
    phone = models.CharField(verbose_name='电话', max_length=32)
    home = models.CharField(verbose_name='地址', max_length=64)
    loves = models.CharField(verbose_name='爱好', max_length=128)


class Customer(models.Model):
    """
    客户表
    """
    name = models.CharField(verbose_name='姓名', max_length=32)
    age = models.CharField(verbose_name='年龄', max_length=32)
    email = models.EmailField(verbose_name='邮箱', max_length=32)
    company = models.CharField(verbose_name='公司', max_length=32)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'customer'
        verbose_name = '客户表'


class Payment(models.Model):
    """
    付费记录
    """
    customer = models.ForeignKey(verbose_name='关联客户', to='Customer', on_delete=models.CASCADE)
    money = models.IntegerField(verbose_name='付费金额')
    create_time = models.DateTimeField(verbose_name='付费时间', auto_now_add=True)

    class Meta:
        db_table = 'payment'
        verbose_name = '付费记录'
