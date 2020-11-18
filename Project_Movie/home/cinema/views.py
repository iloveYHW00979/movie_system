import uuid
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.http import HttpResponse, QueryDict
from rest_framework.views import APIView
from Project_Movie.Util.serializers import SysDataSerializer, CinemaSerializer, ViewingSerializer, OrderSerializer, \
    SeatSerializer
from Project_Movie.home.cinema.models import *
import json
from Project_Movie.Util.utils import response_success, response_failure, paginate_success
from Project_Movie.home.movies.models import SysDictData
from rest_framework.pagination import PageNumberPagination

page = PageNumberPagination()
# 操作影院信息
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
                    data = Cinema.objects.filter(**kwargs).values()
                except Exception as e:
                    raise e
                return response_success(code=200,data=list(data))
        else:
            # 获取所有影院列表信息
            try:
                all_cinemas = Cinema.objects.all().values()
            except :
                return response_failure(code=409)
            return response_success(code=200, data=list(all_cinemas))

    def post(self, request):
        # 添加影院信息
        query_param = json.loads(request.body)
        if query_param:
            try:
                name_list = Cinema.objects.filter(name=query_param.get('name'))
                if name_list:
                    error_info = '%s该影院名称已经存在了' % query_param.get('name')
                    return response_failure(message=error_info)
                else:
                    # 数据保存在数据库中，并返回到登录页面
                    Cinema.objects.create(
                        name=query_param.get('name'),
                        address=query_param.get('address'),
                        tel=query_param.get('tel'),
                        icon=query_param.get('icon'),
                        cinema_brand=query_param.get('cinema_brand'),
                        administrative_district=query_param.get('administrative_district'),
                        special_hall=query_param.get('special_hall'),
                        cinema_service=query_param.get('cinema_service'))
            except Exception as e:
                raise e

            return response_success(code=201)

    def put(self, request):
        # 修改影院信息
        query_param = json.loads(request.body)
        if query_param:
            try:
                cinema = Cinema.objects.get(id=query_param.get('cinema_id'))
                if cinema is None:
                    error_info = '该影院不存在'
                    return response_failure(message=error_info)
                else:
                    serializer = CinemaSerializer(cinema, data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                        return response_success(data=serializer.data)
            except:
                raise
            response_failure(code=409)

    def delete(self, request):
        # 删除影院
        query_param = request.query_params
        if query_param:
            try:
                cinema = Cinema.objects.filter(id=query_param.get('id'))
                if cinema is None:
                    error_info = '该影院不存在'
                    return response_failure(message=error_info)
                else:
                    cinema.delete()
                    return response_success(code=200)
            except:
                raise

# 获取单个影院信息
class CinemaDetail(APIView):
    def get(self, request):
        query_params = request.query_params
        if isinstance(query_params, QueryDict):
            cinema_id = query_params.get('id')
            try:
                cinema_info = Cinema.objects.filter(id=cinema_id).values()
            except Exception as e:
                raise e
            if cinema_info:
                return response_success(data=list(cinema_info))
            else:
                error_info = '该影片不存在'
                return response_failure(message=error_info)

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
        return response_success(data=result_list)

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
                    ret = Seat.objects.filter(view_id=view_id)
                # 根据电影id/日期获取场次信息
                else:
                    movie_id = query_params.get('movie_id')
                    date_time = query_params.get('date')
                    if movie_id and date_time:
                        ret = Viewing.objects.filter(movie_id=movie_id, date_time=date_time)
                    elif movie_id:
                        ret = Viewing.objects.filter(movie_id=movie_id).values()
                    else:
                        error_info = '请求失败，当前影院/电影不存在'
                        return response_failure(error_info)
            except Exception as e:
                raise e
            return response_success(data=list(ret))

    # 添加场次信息
    def post(self, request):
        query_params = json.loads(request.body)
        if query_params:
            movie_id = query_params.get('movie_id')
            view_name = query_params.get('view_name')
            view_start_time = query_params.get('view_start_time')
            view_end_time = query_params.get('view_end_time')
            view_info =Viewing.objects.filter(movie_id=movie_id, view_name=view_name, view_start_time__gte=view_start_time, view_end_time__lte=view_end_time)
            if view_info:
                return response_failure(message='该场次信息已存在')
            try:
                Viewing.objects.create(
                    view_name=query_params.get('view_name'),
                    view_start_time=query_params.get('view_start_time'),
                    view_end_time=query_params.get('view_end_time'),
                    language=query_params.get('language'),
                    price=query_params.get('price'),
                    date_time=query_params.get('date_time'),
                    movie_id=query_params.get('movie_id')
                )
            except :
                raise
            return response_success(code=201)
    # 更新场次信息
    def put(self, request):
        query_param = json.loads(request.body)
        if query_param:
            try:
                view = Viewing.objects.get(id=query_param.get('view_id'))
                if view is None:
                    error_info = '该场次不存在'
                    return response_failure(code=404)
                else:
                    serializer = ViewingSerializer(view, data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                        return response_success(data=serializer.data)
            except:
                raise
            response_failure(code=409)

    #  删除场次
    def delete(self, request):
        query_param = request.query_params
        if query_param:
            try:
                view = Viewing.objects.filter(id=query_param.get('id'))
                if view is None:
                    error_info = '该场次不存在'
                    return response_failure(code=404)
                else:
                    view.delete()
                    return response_success(code=200)
            except:
                raise

# 订单信息
class CinemaOrder(APIView):
    # 获取订单信息
    def get(self, request):
        query_params = request.query_params
        if query_params:
            try:
                order_info = Order.objects.filter(user_id = query_params.get('user_id')).all()
                if order_info:
                    # 创建分页对象
                    page_order = page.paginate_queryset(queryset=order_info, request=request, view=self)  # 获取分页的数据
                    serializer = OrderSerializer(page_order, many=True)
                    return paginate_success(code=200, data=serializer.data, total=order_info.count())
                else:
                    response_failure('该用户没有订单信息')
            except:
                raise
    # 创建订单
    def post(self, request):
        query_params = json.loads(request.body)
        if query_params:
            view_id = query_params.get('view_id')
            seats = query_params.get('seat')
            time = query_params.get('time')
            user_id = query_params.get('user_id')
            movie_id = query_params.get('movie_id')
            cinema_id = query_params.get('cinema_id')
            ticket_num = query_params.get('ticket_num')
            price = query_params.get('price')
            try:
                if view_id:
                    view_info = Viewing.objects.filter(id=view_id)
                    if view_info is None:
                        return response_failure(message='场次不存在')
                else:
                    return response_failure(message='请输入正确的场次')

                if time > view_info.get('view_start_time'):
                    return response_failure(message='该场次已上映')

                db_seats = Seat.objects.get(view_id=view_id)
                for seat in seats:
                    if seat in list(db_seats.seat):
                        return response_failure(message='当前位置已经被选定，请重新选座')
                with transaction.atomic():
                    #更新座位信息
                    serializer = SeatSerializer(db_seats, data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                    else:
                        response_failure('更新座位信息失败')
                    Order.objects.create(
                        order_num=uuid.uuid4(),
                        user_id=user_id,
                        movie_id=movie_id,
                        cinema_id=cinema_id,
                        view_id=view_id,
                        seat=seats,
                        ticket_num=ticket_num,
                        price=price,
                        create_time=time,
                        status=True
                    )
                    data = Order.objects.get('order_num').values()
            except Exception as e:
                raise e

            return response_success(data=list(data), message='创建订单成功')
    #  删除订单
    def delete(self, request):
        query_params = request.query_params
        if query_params:
            try:
                order = Order.objects.get(id=query_params.get('id'))
                if order:
                    order.delete()
                    return response_success(code=200)
                else:
                    response_failure('没有该订单信息')
            except:
                raise

class TestView(APIView):
    pass