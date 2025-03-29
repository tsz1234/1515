from django.db import models

class Products(models.Model):
    id = models.AutoField('id', primary_key=True)
    标题 = models.CharField('标题', max_length=50, default='')
    总价 = models.CharField('总价(万)', max_length=50, default='')
    面积 = models.CharField('面积(㎡)', max_length=50, default='')
    装修 = models.CharField('装修', max_length=50, default='')
    楼层 = models.CharField('楼层', max_length=50, default='')
    年份 = models.CharField('年份', max_length=50, default='')
    小区 = models.CharField('小区', max_length=50, default='')
    区域 = models.CharField('区域', max_length=50, default='')
    关注量 = models.CharField('关注量', max_length=50, default='')
    发布时间 = models.CharField('发布时间', max_length=50, default='')
    户型 = models.CharField('户型', max_length=50, default='')
    单价 = models.CharField('单价(元/平)', max_length=50, default='')
    朝向 = models.CharField('朝向', max_length=50, default='')
    结构 = models.CharField('结构', max_length=50, default='')
    class Meta:
        db_table = "houses"

class User(models.Model):
    id = models.AutoField('id', primary_key=True)
    username = models.CharField('用户名', max_length=50, default='')
    password = models.CharField('密码', max_length=50, default='')
    createTime = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = "users"