from django.http import HttpResponse, JsonResponse
import json
import re
from Project_Movie.Util.utils import response_success, response_failure, \
    paginate_success, CustomPageNumberPagination
from Project_Movie.Util.serializers import InformationSerializer, InformationImgSerializer, AdvertisingSerializer
from Project_Movie.home.information.models import InformationManage, InformationImg, Advertising

from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination


class InformationList(APIView):
    """
    列出所有的资讯或者创建一个新的资讯。
    """

    def get(self, request):
        key_word = request.GET.get('key_word')
        kwargs = {}

        if key_word is not None:
            kwargs['title__contains'] = key_word

        try:
            information = InformationManage.objects.filter(**kwargs).all().order_by('-create_time')
            total = information.count()

            pg = CustomPageNumberPagination()  # 创建分页对象
            page_information = pg.paginate_queryset(queryset=information, request=request, view=self)  # 获取分页的数据
            serializer = InformationSerializer(page_information, many=True)
        except InformationManage.DoesNotExist:
            return response_failure(code=404)
        return paginate_success(code=200, data=serializer.data, total=total)

    def post(self, request):
        serializer = InformationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response_success(code=200)
        return response_failure(code=400)


class InformationDetail(APIView):
    """
    检索，更新或删除一个资讯示例。
    """

    def get(self, request, information_id):
        try:
            information = InformationManage.objects.get(id=information_id)
            serializer = InformationSerializer(information)
        except InformationManage.DoesNotExist:
            return response_failure(code=404)
        return response_success(code=200, data=serializer.data)

    def put(self, request, information_id):

        try:
            information = InformationManage.objects.get(id=information_id)
            serializer = InformationSerializer(information, data=request.data)
        except InformationManage.DoesNotExist:
            return response_failure(code=404)

        if serializer.is_valid():
            serializer.save()
            return response_success(code=200, data=serializer.data)
        return response_failure(code=400)

    def delete(self, request, information_id):

        try:
            information = InformationManage.objects.get(id=information_id)
            information.delete()

        except InformationManage.DoesNotExist:
            return response_failure(code=404)
        return response_success(code=200)


class InformationImgList(APIView):
    """
    根据information_id检索图集或者创建一个新的图集。
    根据information_id修改或者删除图集。
    """

    def get(self, request):
        information_id = request.GET.get('information_id')
        if information_id is None:
            return response_failure(code=400)
        try:
            image = InformationImg.objects.filter(information_id=information_id).all()
            serializer = InformationImgSerializer(image, many=True)
        except InformationImg.DoesNotExist:
            return response_failure(code=404)
        return response_success(code=200, data=serializer.data)

    def put(self, request):
        image_id = request.data.get('image_id')
        if image_id is None:
            return response_failure(code=400)
        try:
            image = InformationImg.objects.get(id=image_id)
            serializer = InformationImgSerializer(image, data=request.data)
        except InformationImg.DoesNotExist:
            return response_failure(code=404)

        if serializer.is_valid():
            serializer.save()
            return response_success(code=200, data=serializer.data)
        return response_failure(code=400)

    def delete(self, request):
        image_id = request.data.get('image_id')
        if image_id is None:
            return response_failure(code=400)
        try:
            image = InformationImg.objects.get(id=image_id)
            image.delete()
        except InformationImg.DoesNotExist:
            return response_failure(code=404)
        return response_success(code=200)

    def post(self, request):
        serializer = InformationImgSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response_success(code=200)
        return response_failure(code=400)


class AdvertisingInfor(APIView):
    """
    检索，更新一个轮播图示例。
    """

    def get(self, request):
        try:
            advertising = Advertising.objects.first()
            serializer = AdvertisingSerializer(advertising)
        except Advertising.DoesNotExist:
            return response_failure(code=404)
        return response_success(code=200, data=serializer.data)

    def put(self, request):
        try:
            advertising = Advertising.objects.first()
            serializer = AdvertisingSerializer(advertising, data=request.data)
        except Advertising.DoesNotExist:
            return response_failure(code=404)

        if serializer.is_valid():
            serializer.save()
            return response_success(code=200, data=serializer.data)
        return response_failure(code=400)


def sort_func(info_list):
    return info_list["info_hot"]


def get_hot_information(request):
    try:
        information = InformationManage.objects.all()
        serializer = InformationSerializer(information, many=True)
        info_list = serializer.data
        hot_info = sorted(info_list, key=sort_func, reverse=True)[:10]
    except InformationManage.DoesNotExist:
        return response_failure(code=404)
    return response_success(code=200, data=hot_info)