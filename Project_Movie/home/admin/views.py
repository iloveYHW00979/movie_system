import base64
import re
from django.db.utils import IntegrityError
from rest_framework.views import APIView
from Project_Movie.Util.serializers import UserSerializer
from Project_Movie.Util.utils import response_failure, response_success
from Project_Movie.home.user.models import *
from Project_Movie.home.user.views import UserPurseView


class RegisterView(APIView):

    def post(self, request):
        # - 获取请求参数
        query_params = request.data
        user_name = query_params.get('user_name')
        password = query_params.get('password')
        password2 = query_params.get('password2')
        # e_mail = query_params.get('e_mail')

        # - 校验数据合法性
        # 所有的参数都不为空时,all方法才会返回True
        if not all([user_name, password, password2]):
            return response_failure('参数不能为空')

        if password != password2:
            return response_failure('两次输入的密码不一致')

        # if not re.match('^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', e_mail):
        #     return response_failure('邮箱格式不正确')

        try:
            user_info = User.objects.filter(user_name=user_name)
            if user_info:
                return response_failure('用户名已存在')
            else:
                data = {
                    'user_name':user_name,
                    'password':base64.b64encode(password.encode('utf-8')).decode('utf-8'),
                    "address":query_params.get('address'),
                    "sex":query_params.get('sex'),
                    "sign":query_params.get('sign'),
                    "e_mail":query_params.get('e_mail'),
                    "icon":query_params.get('icon')
                }
                serializer = UserSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    request = {
                            "user_id": serializer.data.get('id'),
                            "overage": 0
                            }
                    if UserPurseView().post(request):
                        return response_success(code=201)
        except IntegrityError:  # 数据完整性错误
            return response_failure('参数错误')

class LoginView(APIView):

    def post(self, request):
        """处理登录逻辑"""

        # 获取登录请求参数

        query_params = request.data
        user_name = query_params.get('user_name')
        password = query_params.get('password')

        # 校验参数合法性
        if not all([user_name, password]):
            return response_failure('用户名或密码不能为空')
        try:
            user_info = User.objects.filter(user_name=user_name).first()
            if user_info:
                if base64.b64decode(user_info.password.encode('utf-8')).decode('utf-8') != password:
                    return response_failure('登陆密码错误')
                return response_success(code=200, data=UserSerializer(user_info).data)

            else:
                return response_failure('该用户不存在')
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
        pass











