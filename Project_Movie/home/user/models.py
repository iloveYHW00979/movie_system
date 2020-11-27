from django.contrib.auth.models import AbstractUser
from django.db import models

GENDER_CHOICES = (
    (0, '男'),
    (1, '女'),
)
class User(models.Model):
    """用户信息模型类"""
    id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=256, verbose_name=u'用户名', null=True)
    password = models.CharField(max_length=256, verbose_name=u'密码', null=True)
    sex = models.CharField(max_length=256, choices=GENDER_CHOICES, verbose_name=u'性别', null=True)
    e_mail= models.CharField(max_length=256, verbose_name=u'邮箱', null=True)
    address = models.CharField(max_length=256, verbose_name=u'地址', null=True)
    sign = models.CharField(max_length=256, verbose_name=u'签名', null=True)
    icon = models.ImageField(upload_to='static/user', verbose_name='头像', null=True)


    class Meta:
        db_table = 'user'
        verbose_name = '用户表'

class Purse(models.Model):
    """用户钱包表"""
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(verbose_name='用户id',null=True)
    overage = models.FloatField(verbose_name='余额', null=True)

    class Meta:
        db_table = 'purse'
        verbose_name = '用户钱包'







