import re
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.utils import IntegrityError
from django.shortcuts import render
from rest_framework.views import APIView

from Project_Movie.Util.serializers import UserSerializer
from Project_Movie.Util.utils import response_failure, response_success
from Project_Movie.home.user.models import *

class RegisterView(APIView):

    def post(self, request):
        # - 获取请求参数
        query_params = request.query_params
        username = query_params.get('name')
        password = query_params.get('password')
        password2 = query_params.get('password2')
        e_mail = query_params.get('e_mail')


        # - 校验数据合法性
        # 所有的参数都不为空时,all方法才会返回True
        if not all([username, password, password2]):
            return render(request,  {'errmsg': '参数不能为空'})

        if password != password2:
            return render(request, 'register.html', {'errmsg': '两次输入的密码不一致'})

        if not re.match('^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', e_mail):
            return render(request, 'register.html', {'errmsg': '邮箱格式不正确'})

        try:
            user_info = User.objects.filter(name=username)
            if user_info:
                return response_failure('用户名已存在')
            else:
                serializer = UserSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return response_success(code=201)
        except IntegrityError:  # 数据完整性错误
            return response_failure('参数错误')



class LoginView(APIView):

    def post(self, request):
        """处理登录逻辑"""

        # 获取登录请求参数
        query_params = request.data
        name = query_params.get('name')
        password = query_params.get('password')

        # 校验参数合法性
        if not all([name, password]):
            return render(request, 'login.html', {'errmsg': '用户名或密码不能为空'})
        try:
            user_info = User.objects.filter(name=name)
            if user_info:
               return response_success(code=200)
        except:
            raise

        # # 设置session有效期
        # if remember == 'on': # 勾选保存用户登录状态
        #     request.session.set_expiry(None)  # 保存登录状态两周
        # else:
        #     request.session.set_expiry(0)    # 关闭浏览器后,清除登录状态


class LogoutView(APIView):

    def get(self, request):
        """注销功能:清空用户的session数据(用户id)"""

        # 会清除用户id session数据
        logout(request)











