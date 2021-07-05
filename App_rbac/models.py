from django.db import models


class UserInfo(models.Model):
    '''
    用户表
    '''
    name = models.CharField(verbose_name='用户名', max_length=32)
    password = models.CharField(verbose_name='密码', max_length=64)
    email = models.CharField(verbose_name='邮箱', max_length=64)
    roles = models.ManyToManyField(verbose_name='所有角色', to='Role', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'userinfo'
        verbose_name = '用户'


class Permission(models.Model):
    '''
    权限表
    '''
    title = models.CharField(verbose_name='标题', max_length=32)
    url = models.CharField(verbose_name='url', max_length=128)
    name = models.CharField(verbose_name="URL别名", max_length=32, unique=True)
    # 菜单的划分
    menu = models.ForeignKey(verbose_name='所属菜单', to='Menu',null=True, blank=True,
                             help_text='null表示不是菜单,这个字段有值才表示二级菜单',
                             on_delete=models.DO_NOTHING)
    pid = models.ForeignKey('self', verbose_name='关联某个权限',
                            help_text='对于非菜单权限需要选择一个可以成为菜单的权限,用户做默认展开和选中的菜单',
                            null=True, blank=True, on_delete=models.DO_NOTHING, related_name='parents')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'permission'
        verbose_name = '权限'


class Menu(models.Model):
    title = models.CharField(verbose_name='一级菜单', max_length=32)
    icon = models.CharField(verbose_name='菜单图标', max_length=32, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'menu'
        verbose_name = '菜单'


class Role(models.Model):
    '''
    角色表
    '''
    title = models.CharField(verbose_name='角色名称', max_length=32)
    permission = models.ManyToManyField(verbose_name='拥有的权限', to='Permission', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'role'
        verbose_name = '角色'
