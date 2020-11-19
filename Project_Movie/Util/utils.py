import json
import datetime
from django.http import HttpResponse
from rest_framework.pagination import PageNumberPagination

from Project_Movie import settings
import random

# 返回状态码及信息
status_code = {
    200: '操作成功',
    201: '对象创建成功',
    202: '请求已经被接受',
    204: '操作已经执行成功，但是没有返回数据',
    301: '资源已被移除',
    303: '重定向',
    304: '资源没有被修改',
    400: '参数列表错误（缺少，格式不匹配)',
    401: '未授权',
    403: '访问受限，授权过期',
    404: '资源，服务未找到',
    405: '不允许的http方法',
    409: '资源冲突，或者资源被锁',
    415: '不支持的数据，媒体类型',
    500: '系统内部错误',
    501: '接口未实现'
}


# json 工具类
class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, datetime.time):
            return obj.strftime('%H:%M:%S')
        return json.JSONEncoder.default(self, obj)


# 查询成功
def response_success(code=None, message=None, data=None):
    message = status_code.get(code)
    return HttpResponse(json.dumps({
        'code': code,  # code由前后端配合指定
        'msg': message,  # 提示信息
        'data': data,  # 返回数据
        # 'count': len(data )# 总条数
    }, cls=JSONEncoder), 'application/json')


# 查询失败
def response_failure(code=None, message=None):
    message = status_code.get(code)
    return HttpResponse(json.dumps({
        'code': code,
        'msg': message
    }), 'application/json')


# 分页查询成功
def paginate_success(code=None, message=None, data=None, total=0):
    message = status_code.get(code)
    return HttpResponse(json.dumps({
        'total': total,  # 总页数
        'code': code,  # code由前后端配合指定
        'msg': message,  # 提示信息
        'rows': data,  # 返回数据
    }, cls=JSONEncoder), 'application/json')

# 分页页数问题
class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'size'

# # 上传图片
# def upload_image(img_file):
#     # 获取后缀名
#     ext = img_file.name.split('.')[-1]
#     # 如果上传图片的后缀名不在配置的后缀名里返回格式不允许
#     if ext not in settings.ALLOWED_IMG_TYPE:
#         return response_failure(code=415)
#     # 新的文件名
#     new_file_name = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + str(
#         random.randint(10000, 99999)) + '.' + ext  # 采用时间和随机数
#     path = settings.UPLOAD_ADDRESS + new_file_name
#     with open(path, 'wb') as f:  # 二进制写入
#         for i in img_file.chunks():
#             f.write(i)
#     return path
