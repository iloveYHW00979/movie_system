from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.views import APIView

from Project_Movie.Util.serializers import UserSerializer
from Project_Movie.Util.utils import response_failure, response_success
from Project_Movie.home.user.models import *

class UserInfoView(LoginRequiredMixin, APIView):

    def get(self, request):
        """进入用户个人信息界面"""

        user_id = request.query_params.get('id')  # 登录用户
        try:
            data = User.objects.filter(id=user_id).values()
        except Exception as e:
            raise e
        return response_success(data=data)


class UserOrderView(LoginRequiredMixin, APIView):

    def get(self, request):
        """进入用户订单界面"""
        pass











