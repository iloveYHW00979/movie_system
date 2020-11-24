from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.views import APIView

from Project_Movie.Util.serializers import UserSerializer, CommentSerializer, PurseSerializer, FavoriteSerializer
from Project_Movie.Util.utils import response_failure, response_success, CustomPageNumberPagination, paginate_success
from Project_Movie.home.cinema.models import Order
from Project_Movie.home.movies.models import Comment, Favorite
from Project_Movie.home.user.models import *

class UserInfoView(APIView):

    def get(self, request):
        """进入用户个人信息界面"""
        user_id = request.query_params.get('id')  # 登录用户
        try:
            if user_id:
                data = User.objects.filter(id=user_id).order_by('id')
                if len(data) == 0:
                    return response_failure('没有该id的用户')
            else:
                data = User.objects.all().order_by('id')
        except Exception as e:
            raise e
        if data:
            # 创建分页对象
            page_order = CustomPageNumberPagination().paginate_queryset(queryset=data, request=request,                                                             view=self)  # 获取分页的数据
            serializer = UserSerializer(page_order, many=True)
            return paginate_success(code=200, data=serializer.data, total=data.count())

    def put(self, request):
        """更新用户信息"""
        query_params = request.data
        user_id = query_params.get('id')
        password = query_params.get('password')
        if password == '':
            return response_failure('密码不能为空')
        try:
            user_info = User.objects.filter(id=user_id).first()
            if user_info:
                serializer = UserSerializer(user_info, request.data)
                if serializer.is_valid():
                    serializer.save()
                else:
                    return response_failure('保存数据失败')
            else:
                return response_failure('没有该用户id')
        except Exception as e:
            raise e
        return response_success(code=200)

    def delete(self, request):
        """删除用户信息"""
        user_id = request.query_params.get('id')
        if user_id:
            try:
                user_info = User.objects.filter(id=user_id)
                order = Order.objects.filter(user_id=user_id)
                if user_info:
                    user_info.delete()
                else:
                    return response_failure('没有该用户id')
                if order:
                    order.delete()
                return response_success(code=200)
            except:
                return response_failure('数据库操作错误:没有该用户')

class UserPurseView(APIView):

    def get(self, request):
        """获取我的钱包余额"""
        user_id =  request.query_params.get('user_id')
        if user_id:
            try:
                data = Purse.objects.filter(user_id=user_id).first()
            except:
                raise
            if data:
                serializer = PurseSerializer(data)
            else:
                return response_failure('没有该用户的余额信息')
        else:
            return response_failure('请输入用户id')
        return response_success(code=200,data=serializer.data)

    def post(self, request):
        """充值余额"""
        user_id = request.data.get('user_id')
        overage = request.data.get('overage')
        if user_id and overage:
            try:
                user = User.objects.filter(id=user_id)
            except:
                raise
            if user:
                serializer = PurseSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                else:
                    return response_failure('数据存储失败')
            else:
                return response_failure('没有该用户信息')
            return response_success(code=201, data=serializer.data)

    def put(self, request):
        user_id = request.data.get('user_id')
        overage = request.data.get('overage')
        if user_id and overage:
            try:
                purse = Purse.objects.filter(user_id=user_id).first()
            except:
                raise
            if purse:
                overage = float(overage) + purse.overage
                data = {
                    "overage":overage
                }
                serializer = PurseSerializer(purse, data=data)
                if serializer.is_valid():
                    serializer.save()
                else:
                    return response_failure('数据库更新失败')
            else:
                return response_failure('没有该用户的余额信息')
            return response_success(code=200, data=serializer.data)

class UserCommentView(APIView):
    """获取用户评论"""
    def get(self, request):
        query_params = request.query_params
        user_id = query_params.get('user_id')
        movie_id = query_params.get('movie_id')
        if query_params:
            if user_id and movie_id:
                data = Comment.objects.filter(user_id=user_id, movie_id=movie_id).order_by('id')
            elif user_id:
                data = Comment.objects.filter(user_id=user_id).order_by('id')
            else:
                return response_failure('参数错误')
            if data:
                # 创建分页对象
                page_order = CustomPageNumberPagination().paginate_queryset(queryset=data, request=request, view=self)  # 获取分页的数据
                serializer = CommentSerializer(page_order, many=True)
                return paginate_success(code=200, data=serializer.data, total=data.count())
            else:
                return response_failure('当前用户没有对应评论')

class UserCollectView(APIView):
    """用户收藏列表"""
    def get(self, request):
        user_id = request.query_params.get('user_id')
        if user_id:
            try:
                collect = Favorite.objects.filter(user_id=user_id).order_by('id')
            except:
                raise
            if collect:
                # 创建分页对象
                page_order = CustomPageNumberPagination().paginate_queryset(queryset=collect, request=request, view=self)  # 获取分页的数据
                serializer = FavoriteSerializer(page_order, many=True)
                return paginate_success(code=200, data=serializer.data, total=collect.count())
            else:
                return response_failure('当前用户收藏电影')
        else:
            return response_failure('请输入要查询的用户id')
