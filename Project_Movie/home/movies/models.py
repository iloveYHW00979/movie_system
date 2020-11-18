from django.db import models


# Create your models here.
# 电影列表
class Movies(models.Model):

    id = models.AutoField(primary_key=True, verbose_name='电影id')
    create_time = models.DateTimeField(verbose_name='创建时间', null=True)
    update_time = models.DateTimeField(verbose_name='更新时间', null=True)
    delete_time = models.DateTimeField(verbose_name='删除时间', null=True)
    movie_name = models.CharField(max_length=32, verbose_name='电影名称')
    movie_score = models.FloatField(verbose_name='评分', null=True)
    movie_poster = models.CharField(max_length=255, verbose_name='海报', null=True)
    movie_type = models.IntegerField(verbose_name='类型（关联基础数据表）')
    movie_region = models.IntegerField(verbose_name='区域（关联基础数据表）')
    movie_duration = models.IntegerField(verbose_name='时长', null=True)
    movie_release_date = models.DateTimeField(verbose_name='上映时间', null=True)
    movie_era = models.IntegerField(verbose_name='年代（关联基础数据表）')
    movie_description = models.CharField(max_length=255, verbose_name='剧情介绍')
    movie_score_num = models.IntegerField(verbose_name='评分人数', null=True)
    movie_box_office = models.DecimalField(max_digits=11, decimal_places=2, verbose_name='票房', null=True)
    movie_anticipate = models.IntegerField(verbose_name='想看数', null=True)
    movie_status = models.IntegerField(verbose_name='电影状态（关联基础数据表）')
    movie_hot = models.IntegerField(verbose_name='热度（订单数）')

    class Meta:
        db_table = 'movies'
        verbose_name = '电影'


class Comment(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='评论id')
    movie_id = models.IntegerField(verbose_name=u'电影id')
    user_id = models.IntegerField(verbose_name=u'用户id')
    create_time = models.DateTimeField(verbose_name=u'创建时间', null=True)
    update_time = models.DateTimeField(verbose_name=u'更新时间', null=True)
    delete_time = models.DateTimeField(verbose_name=u'删除时间', null=True)
    score = models.IntegerField(verbose_name=u'评分')
    content = models.TextField(null=True, verbose_name=u'评论')

    class Meta:
        # abstract = True
        db_table = 'comment'
        verbose_name = u'电影评论'


# 演职人员
class Cast(models.Model):

    id = models.AutoField(primary_key=True, verbose_name='演职人员id')
    create_time = models.DateTimeField(verbose_name='创建时间', null=True)
    update_time = models.DateTimeField(verbose_name='更新时间', null=True)
    delete_time = models.DateTimeField(verbose_name='删除时间', null=True)
    movie_id = models.IntegerField(verbose_name='电影id）')
    cast_picture = models.CharField(max_length=255, verbose_name='人员图片')
    cast_name = models.CharField(max_length=32, verbose_name='姓名')
    role = models.CharField(max_length=32, verbose_name='饰演角色', null=True)
    cast_type = models.IntegerField(verbose_name='人员类型（关联基础数据表）')

    class Meta:
        db_table = 'cast'
        verbose_name = '演职人员'


# 电影图集
class MovieImages(models.Model):

    id = models.AutoField(primary_key=True, verbose_name='图片id')
    create_time = models.DateTimeField(verbose_name='创建时间', null=True)
    update_time = models.DateTimeField(verbose_name='更新时间', null=True)
    delete_time = models.DateTimeField(verbose_name='删除时间', null=True)
    movie_id = models.CharField(max_length=128, verbose_name='电影id')
    image = models.CharField(max_length=255, verbose_name='图片')

    class Meta:
        db_table = 'movie_images'
        verbose_name = '电影图集'


# 基础数据类型
class SysDictType(models.Model):

    dict_id = models.AutoField(primary_key=True, verbose_name='字典主键')
    dict_name = models.CharField(max_length=100, verbose_name='字典名称')
    dict_type = models.CharField(max_length=100, verbose_name='字典类型')
    status = models.IntegerField(verbose_name='状态（0正常 1停用）')
    create_by = models.CharField(max_length=64, verbose_name='创建者')
    create_time = models.DateTimeField(verbose_name='创建时间', null=True)
    update_by = models.CharField(max_length=64, verbose_name='更新者')
    update_time = models.DateTimeField(verbose_name='更新时间', null=True)
    remark = models.CharField(max_length=500, verbose_name='备注')

    class Meta:
        db_table = 'sys_dict_type'
        verbose_name = '基础数据类型'


# 基础数据
class SysDictData(models.Model):

    dict_code = models.AutoField(primary_key=True, verbose_name='字典编码')
    dict_sort = models.IntegerField(verbose_name='字典排序')
    dict_label = models.CharField(max_length=100, verbose_name='字典标签')
    dict_value = models.CharField(max_length=100, verbose_name='字典键值')
    dict_type = models.CharField(max_length=100, verbose_name='字典类型')
    css_class = models.CharField(max_length=100, verbose_name='样式属性（其他样式扩展）')
    list_class = models.CharField(max_length=100, verbose_name='表格回显样式')
    is_default = models.CharField(max_length=1, verbose_name='是否默认（Y是 N否）')
    status = models.IntegerField(verbose_name='状态（0正常 1停用）')
    create_by = models.CharField(max_length=64, verbose_name='创建者')
    create_time = models.DateTimeField(verbose_name='创建时间', null=True)
    update_by = models.CharField(max_length=64, verbose_name='更新者')
    update_time = models.DateTimeField(verbose_name='更新时间', null=True)
    remark = models.CharField(max_length=500, verbose_name='备注')

    class Meta:
        db_table = 'sys_dict_data'
        verbose_name = '基础数据'
