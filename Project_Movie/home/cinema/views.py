import uuid
import time
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.http import HttpResponse, QueryDict
from rest_framework.views import APIView
from Project_Movie.Util.serializers import SysDataSerializer, CinemaSerializer, ViewingSerializer, OrderSerializer, \
    SeatSerializer, PurseSerializer
from Project_Movie.home.cinema.models import *
import json
from Project_Movie.Util.utils import response_success, response_failure, paginate_success, CustomPageNumberPagination
from Project_Movie.home.movies.models import SysDictData
from rest_framework.pagination import PageNumberPagination

# 操作影院信息
from Project_Movie.home.user.models import Purse


class CinemaView(APIView):
    # 获取某个属性下的影院信息
    def get(self, request):
        query_param = request.query_params
        if query_param:
            if isinstance(query_param, QueryDict):
                cinema_brand = query_param.get('cinema_brand')
                administrative_district = query_param.get('administrative_district')
                special_hall = query_param.get('special_hall')
                cinema_service = query_param.get('cinema_service')
                kwargs = {}
                if cinema_brand:
                    kwargs['cinema_brand'] = cinema_brand
                if administrative_district:
                    kwargs['administrative_district'] = administrative_district
                if special_hall:
                    kwargs['special_hall'] = special_hall
                if cinema_service:
                    kwargs['cinema_service'] = cinema_service
                try:
                    data = Cinema.objects.filter(**kwargs).order_by('id')
                except Exception as e:
                    raise e
                if data:
                    # 创建分页对象
                    page_order = CustomPageNumberPagination().paginate_queryset(queryset=data, request=request, view=self)  # 获取分页的数据
                    serializer = CinemaSerializer(page_order, many=True)
                    return paginate_success(code=200, data=serializer.data, total=data.count())
                else:
                    return response_failure('当前属性下没有对应的数据')
        else:
            # 获取所有影院列表信息
            try:
                all_cinemas = Cinema.objects.all().order_by('id')
            except:
                return response_failure(code=409)
            if all_cinemas:
                # 创建分页对象
                page_order = CustomPageNumberPagination().paginate_queryset(queryset=all_cinemas, request=request, view=self)  # 获取分页的数据
                serializer = CinemaSerializer(page_order, many=True)
                return paginate_success(code=200, data=serializer.data, total=all_cinemas.count())
            else:
                return response_failure('当前没有影院列表')

    def post(self, request):
        # 添加影院信息
        query_param = request.data
        if query_param:
            try:
                name_list = Cinema.objects.filter(name=query_param.get('name'))
                if name_list:
                    error_info = '%s该影院名称已经存在了' % query_param.get('name')
                    return response_failure(message=error_info)
                else:
                    # 数据保存在数据库中
                    serializer = CinemaSerializer(data=query_param)
                    if serializer.is_valid():
                        serializer.save()
                    else:
                        return response_failure('添加影院信息失败')
            except Exception as e:
                raise e
            return response_success(code=201)

    def put(self, request):
        # 修改影院信息
        query_param = request.data
        if query_param:
            try:
                cinema = Cinema.objects.filter(id=query_param.get('cinema_id')).first()
                if cinema is None:
                    return response_failure('该影院不存在')
                else:
                    serializer = CinemaSerializer(cinema, data=query_param)
                    if serializer.is_valid():
                        serializer.save()
                    else:
                        return response_failure('数据库更新失败')
            except:
                raise
            return response_success(code=200)

    def delete(self, request):
        # 删除影院
        query_param = request.query_params
        if query_param:
            try:
                cinema = Cinema.objects.filter(id=query_param.get('id'))
            except:
                raise
            if cinema is None:
                error_info = '该影院不存在'
                return response_failure(message=error_info)
            else:
                cinema.delete()
                return response_success(code=200)


# 获取单个影院信息
class CinemaDetail(APIView):
    def get(self, request):
        query_params = request.query_params
        if isinstance(query_params, QueryDict):
            cinema_id = query_params.get('id')
            if cinema_id:
                try:
                    cinema_info = Cinema.objects.filter(id=cinema_id).first()
                except Exception as e:
                    raise e
                if cinema_info:
                    serializer = CinemaSerializer(cinema_info)
                    return response_success(code=200, data=serializer.data)
                else:
                    return response_failure('该影片不存在')

# 获取所有影院属性
class AttributeView(APIView):
    def get(self, request):
        type_list = ['cinema_brand', 'administrative_district', 'special_hall', 'cinema_service']
        try:
            dict_data = SysDictData.objects.filter(dict_type__in=type_list, status=0).order_by('dict_sort').all()
            serializer = SysDataSerializer(dict_data, many=True)
            cinema_brand_list = [element for element in serializer.data if element['dict_type'] == 'cinema_brand']
            administrative_district_list = [element for element in serializer.data if element['dict_type'] == 'administrative_district']
            special_hall_list = [element for element in serializer.data if element['dict_type'] == 'special_hall']
            cinema_service_list = [element for element in serializer.data if element['dict_type'] == 'cinema_service']
            result_list = {
                'cinema_brand_list': cinema_brand_list,
                'administrative_district_list': administrative_district_list,
                'special_hall_list': special_hall_list,
                'cinema_service_list': cinema_service_list,
            }
        except ObjectDoesNotExist:
            return response_failure(404, '查询对象结果为空')
        return response_success(code=200, data=result_list)

# 影院场次
class CinemaViewing(APIView):
    # 获取场次信息
    def get(self, request):
        query_params = request.query_params
        if isinstance(query_params, QueryDict):
            view_id = query_params.get('view_id')
            # 根据场次id获取当前场次的座位信息
            try:
                if view_id:
                    view = Viewing.objects.filter(id=view_id).first()
                    if view:
                        seats = Seat.objects.filter(view_id=view_id).first()
                        serializer = SeatSerializer(seats)
                        if seats is None:
                            return response_failure('该场次下没有座位信息')
                        return response_success(code=200, data=serializer.data)
                    else:
                        return response_failure('当前场次不存在')
                # 根据电影id/日期获取场次信息
                else:
                    movie_id = query_params.get('movie_id')
                    date_time = query_params.get('date')
                    cinema_id = query_params.get('cinema_id')
                    if movie_id and date_time and cinema_id:
                        view = Viewing.objects.filter(movie_id=movie_id, date_time=date_time, cinema_id=cinema_id)
                    elif movie_id:
                        view = Viewing.objects.filter(movie_id=movie_id, cinema_id=cinema_id).order_by('view_start_time')
                    else:
                        error_info = '请求失败，当前影院/电影不存在'
                        return response_failure(error_info)
                    serializer = ViewingSerializer(view, many=True)
            except Exception as e:
                raise e
            return response_success(code=200, data=serializer.data)

    # 添加场次信息
    def post(self, request):
        query_params = request.data
        if query_params:
            movie_id = query_params.get('movie_id')
            view_name = query_params.get('view_name')
            view_start_time = query_params.get('view_start_time')
            view_end_time = query_params.get('view_end_time')
            view_info =Viewing.objects.filter(movie_id=movie_id, view_name=view_name, view_start_time__gte=view_start_time, view_end_time__lte=view_end_time)
            if view_info:
                return response_failure(message='该场次信息已存在')
            try:
                serializer = ViewingSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                else:
                    return response_failure('数据库保存失败')
            except :
                raise
            return response_success(code=201)
    # 更新场次信息
    def put(self, request):
        query_param = request.data
        if query_param:
            try:
                view = Viewing.objects.get(id=query_param.get('id'))
                if view is None:
                    return response_failure(code=404, message='该场次不存在')
                else:
                    serializer = ViewingSerializer(view, data=query_param)
                    if serializer.is_valid():
                        serializer.save()
                    else:
                        return response_failure('存储到数据库失败')
            except:
                raise
            return response_success(code=200, data=serializer.data)

    #  删除场次
    def delete(self, request):
        query_param = request.query_params
        if query_param:
            try:
                view = Viewing.objects.filter(id=query_param.get('id'))
            except:
                raise
            if view is None:
                error_info = '该场次不存在'
                return response_failure(code=404)
            else:
                view.delete()
                return response_success(code=200)


# 订单信息
class CinemaOrder(APIView):
    # 获取订单信息
    def get(self, request):
        query_params = request.query_params
        user_id = query_params.get('user_id')
        order_num = query_params.get('order_num')
        try:
            if query_params:
                if user_id and order_num:
                    # 查询该用户的某个订单信息
                    order_info = Order.objects.filter(user_id=user_id, order_num=order_num)
                elif user_id:
                    # 查询该用户的所有订单信息
                    order_info = Order.objects.filter(user_id = user_id).order_by('id')
                elif order_num:
                    # 查询某个订单
                    order_info = Order.objects.filter(order_num=order_num).order_by('id')
                else:
                    # 查询所有订单
                    order_info = Order.objects.all().order_by('id')
                if order_info:
                    # 创建分页对象
                    page_order = CustomPageNumberPagination().paginate_queryset(queryset=order_info, request=request, view=self)  # 获取分页的数据
                    serializer = OrderSerializer(page_order, many=True)
                else:
                    return response_failure('该用户没有订单信息')
        except:
            raise
        return paginate_success(code=200, data=serializer.data, total=order_info.count())
    # 创建订单
    def post(self, request):
        query_params = request.data
        if query_params:
            view_id = query_params.get('view_id')
            seats = query_params.get('seat')
            # create_time = time.time()
            create_time = query_params.get('create_time')
            user_id = query_params.get('user_id')
            movie_id = query_params.get('movie_id')
            cinema_id = query_params.get('cinema_id')
            ticket_num = query_params.get('ticket_num')
            price = query_params.get('price')
            try:
                if view_id:
                    view_info = Viewing.objects.filter(id=view_id).first()
                    if view_info is None:
                        return response_failure(message='场次不存在')
                else:
                    return response_failure(message='请输入正确的场次')
                # 获取座位信息
                db_seats = Seat.objects.filter(view_id=view_id).first()
                with transaction.atomic():
                    # 更新座位信息
                    if db_seats:
                        db_seat = json.loads(db_seats.seat)
                        for seat in json.loads(seats):
                            cur_seat = db_seat[seat[0]][seat[1]]
                            if cur_seat == 1:
                                db_seat[seat[0]][seat[1]] = 2
                            else:
                              return response_failure('当前位置已经被选定，请重新选座')
                        db_seats.seat = str(db_seat)
                    else:
                        return response_failure('该场次没有座位')
                    # 用户钱包减掉余额
                    purse = Purse.objects.filter(user_id=user_id).first()
                    if purse:
                        if float(price) > purse.overage:
                            return response_failure('用户当前余额不够支付该订单')
                        else:
                            overage = purse.overage - float(price)
                            data = {
                                "overage":overage
                            }
                            serializer = PurseSerializer(purse, data=data)
                            if serializer.is_valid() is False:
                                return response_failure('数据库存储失败')
                    else:
                        return response_failure('当前用户没有充值的余额记录')
                    order_no = str(time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))) + str(time.time()).replace('.', '')[-7:]
                    order_info = Order.objects.create(
                        order_num=order_no,
                        user_id=user_id,
                        movie_id=movie_id,
                        cinema_id=cinema_id,
                        view_id=view_id,
                        seat=seats,
                        ticket_num=ticket_num,
                        price=price,
                        create_time=create_time,
                        status=True
                    )
                    db_seats.save()
                    order_info.save()
                    serializer.save()
                    order = Order.objects.filter(create_time=create_time).first()
                    if order.order_num is None:
                        return response_failure('获取订单编号失败')
            except Exception as e:
                raise e
            return response_success(code=201,data=order.order_num)
    #  删除订单
    def delete(self, request):
        query_params = request.query_params
        if query_params:
            try:
                order = Order.objects.filter(id=query_params.get('id')).first()
                if order:
                    order.delete()
                    return response_success(code=200)
                else:
                    return response_failure('没有该订单信息')
            except:
                raise

class SeatView(APIView):
    """创建/更新座位信息"""
    def post(self, request):
        data = request.data
        if data:
            try:
                view = Viewing.objects.filter(id=data.get('view_id')).first()
                if view:
                    view_seat = Seat.objects.filter(view_id=data.get('view_id')).first()
                    serializer = SeatSerializer(view_seat, data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                else:
                    return response_failure('场次不存在')
            except:
                raise
            return response_success(code=201)

class SearchView(APIView):
    """模糊查询影院信息"""
    def get(self, request):
        query_params = request.query_params
        if query_params:
            try:
                cinema = Cinema.objects.filter(name__contains=query_params.get('cinema_name')).order_by('id')
            except:
                raise
            if cinema:
                # 创建分页对象
                page_order = CustomPageNumberPagination().paginate_queryset(queryset=cinema, request=request, view=self)  # 获取分页的数据
                serializer = CinemaSerializer(page_order, many=True)
                return paginate_success(code=200, data=serializer.data, total=cinema.count())
            else:
                return response_failure('当前没有该影院名称')

class AllViewings(APIView):
    """查询某个影院下所有的场次信息"""
    def get(self, request):
        cinema_id = request.query_params.get('cinema_id')
        try:
            view = Viewing.objects.filter(cinema_id=cinema_id).values().order_by('id')
            page_order = CustomPageNumberPagination().paginate_queryset(queryset=view, request=request, view = self)  # 获取分页的数据
        except:
            raise
        return paginate_success(code=200, data=list(page_order), total=view.count())


        # return response_success(code=200, data=list(view))