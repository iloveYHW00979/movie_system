from django.db import models

class Cinema(models.Model):
    name = models.CharField(max_length=255, verbose_name=u'影院名称', null=True)
    address = models.CharField(max_length=255, verbose_name=u'影院地址', null=True)
    tel = models.CharField(max_length=255, verbose_name=u'影院电话', null=True)
    icon = models.ImageField(upload_to='static/cinema', verbose_name=u'影院图标', null=True)
    cinema_brand = models.IntegerField(verbose_name=u'品牌', null=True)
    administrative_district = models.IntegerField(verbose_name=u'行政区', null=True)
    special_hall = models.IntegerField(verbose_name=u'特殊厅', null=True)
    cinema_service = models.IntegerField(verbose_name=u'服务', null=True)
    class Meta:
        # abstract = True
        db_table = 'cinema'
        verbose_name = u'影院'

class Viewing(models.Model):
    view_name = models.CharField(max_length=256, verbose_name='放映厅名称')
    view_start_time = models.TimeField(verbose_name=u'放映开始时间')
    view_end_time = models.TimeField(verbose_name=u'放映结束时间')
    language = models.CharField(max_length=64, verbose_name=u'电影语言')
    price = models.FloatField(verbose_name=u'电影单价', null=True)
    movie_id = models.IntegerField(verbose_name=u'电影id')
    date_time = models.DateTimeField(verbose_name=u'日期', null=True)
    cinema_id = models.IntegerField(verbose_name='影院id', null=True)
    movie_name = models.CharField(max_length=256, verbose_name='电影名称', null=True)
    class Meta:
        # abstract = True
        db_table = 'viewing'
        verbose_name = u'放映厅'

class Seat(models.Model):
    view_id = models.IntegerField(verbose_name=u'场次id', null=True)
    seat = models.TextField(verbose_name=u'座位', null=True)
    class Meta:
        # abstract = True
        db_table = 'seat'
        verbose_name = u'影厅座位'

class Order(models.Model):
    order_num = models.TextField(verbose_name='订单号')
    user_id = models.IntegerField(verbose_name='用户id')
    movie_id = models.IntegerField(verbose_name='电影id')
    cinema_id = models.IntegerField(verbose_name='影院id')
    view_id = models.IntegerField(verbose_name='场次id')
    seat = models.CharField(max_length=256, verbose_name='座位')
    ticket_num = models.IntegerField(verbose_name='票数')
    price = models.CharField(max_length=256, verbose_name='价格')
    create_time = models.DateTimeField(verbose_name='下单时间')
    status = models.BooleanField(verbose_name='订单状态 0:未支付 1:已支付')
    class Meta:
        # abstract = True
        db_table = 'order'
        verbose_name = u'订单'
