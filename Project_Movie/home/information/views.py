from django.http import HttpResponse, JsonResponse
import json
from Project_Movie.Util.utils import response_success, response_failure, paginate_success
from Project_Movie.Util.serializers import InformationSerializer
from Project_Movie.home.information.models import InformationManage, InformationImg

from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination


class InformationList(APIView):
    """
    列出所有的资讯或者创建一个新的资讯。
    """

    def get(self, request):

        information = InformationManage.objects.all()
        total = information.count()

        pg = PageNumberPagination()  # 创建分页对象
        page_information = pg.paginate_queryset(queryset=information, request=request, view=self)  # 获取分页的数据
        serializer = InformationSerializer(page_information, many=True)
        return paginate_success(code=200, data=serializer.data, total=total)

    def post(self, request):
        serializer = InformationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response_success(code=201)
        return response_failure(code=400)


class InformationDetail(APIView):
    """
    检索，更新或删除一个资讯示例。
    """

    def get(self, request, information_id):
        try:
            information = InformationManage.objects.get(id=information_id)
            serializer = InformationSerializer(information)
            img_list = InformationImg.objects.filter(information_id=information_id).all().values('img_url')
            result = {
                'information_data': serializer.data,
                'img_data': list(img_list)
            }
        except InformationManage.DoesNotExist:
            return response_failure(code=404)
        return response_success(code=200, data=result)

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
            information_img = InformationImg.objects.filter(information_id=information_id).all()
            
        except InformationManage.DoesNotExist:
            return response_failure(code=404)
        return response_success(code=200)

