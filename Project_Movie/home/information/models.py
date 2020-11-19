# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.utils import timezone


class InformationImg(models.Model):
    information_id = models.IntegerField(null=True, verbose_name='资讯id')
    img_url = models.ImageField(upload_to='static/imformation', verbose_name='图片', null=True)

    class Meta:
        managed = False
        db_table = 'information_img'
        verbose_name = '资讯图片'


class InformationManage(models.Model):
    title = models.CharField(max_length=50, verbose_name='标题', null=True)
    content = models.CharField(max_length=500, verbose_name='内容', null=True)
    create_time = models.DateTimeField(null=True, verbose_name='创建时间', default=timezone.now)
    img_url = models.ImageField(upload_to='static/imformation', verbose_name='图片', null=True)
    issuer = models.CharField(max_length=50, null=True, verbose_name='发布者')

    class Meta:
        managed = False
        db_table = 'information_manage'
        verbose_name = '资讯'


class Advertising(models.Model):
    img_url = models.ImageField(upload_to='static/imformation', verbose_name='图片', null=True)
    img_link = models.CharField(max_length=255, null=True, verbose_name='跳转链接')

    class Meta:
        managed = False
        db_table = 'advertising'
        verbose_name = '首页轮播图'
