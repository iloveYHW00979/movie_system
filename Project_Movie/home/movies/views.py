from Project_Movie.Util.utils import response_success, response_failure
from django.core.exceptions import ObjectDoesNotExist

from Project_Movie.home.movies.models import Movies, SysDictData
from Project_Movie.Util.serializers import MoviesSerializer

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404


# 所有电影
class MoviesList(APIView):

    def get(self, request):
        movies = Movies.objects.all()
        serializer = MoviesSerializer(movies, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MoviesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 根据id查询
class MovieDetail(APIView):
    def get_object(self, movie_id):
        try:
            return Movies.objects.get(id=movie_id)
        except Movies.DoesNotExist:
            raise Http404

    def get(self, request, movie_id):
        movie = self.get_object(movie_id)
        serializer = MoviesSerializer(movie)
        return Response(serializer.data)

    def put(self, request, movie_id):
        movie = self.get_object(movie_id)
        serializer = MoviesSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, movie_id):
        snippet = self.get_object(movie_id)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# 查询所有电影信息
def get_all_movies(request):
    try:
        movies = Movies.objects.all().values()
    except ObjectDoesNotExist:
        return response_failure(10002, '查询对象结果为空')
    return response_success(data=list(movies))


# 根据id查询电影信息
def get_movie(request, movie_id):
    try:
        movie = Movies.objects.filter(id=movie_id).values()
    except ObjectDoesNotExist:
        return response_failure(10023, '查询对象结果为空')
    return response_success(data=list(movie))


# 添加电影信息
def create_movie(request):
    if request.method == 'POST':
        movie_name = request.POST.get('movie_name')
        movie_poster = request.POST.get('movie_poster')
        movie_type = request.POST.get('movie_type')
        movie_region = request.POST.get('movie_region')
        movie_duration = request.POST.get('movie_duration')
        movie_era = request.POST.get('movie_era')
        movie = Movies.objects.filter(movie_name=movie_name)
        if movie:
            return response_failure(10001, '数据已存在')
        else:
            try:
                dic = {'movie_name': movie_name,
                       'movie_poster': movie_poster,
                       'movie_type': movie_type,
                       'movie_region': movie_region,
                       'movie_duration': movie_duration,
                       'movie_era': movie_era,
                       }
                Movies.objects.create(**dic)
            except Exception as e:
                raise e
            return response_success(message="创建成功")


# 根据类型查询基础数据
def get_sys_dict(request, dict_type):
    try:
        dict_data = SysDictData.objects.filter(dict_type=dict_type).values()
    except ObjectDoesNotExist:
        return response_failure(10023, '查询对象结果为空')
    return response_success(data=list(dict_data))


# 电影首页基础数据
def get_movie_dict(request):
    type_list = ['movie_status', 'movie_type', 'movie_region', 'movie_era', 'cast_type']
    try:
        dict_data = SysDictData.objects.filter(dict_type__in=type_list, status=0).values()
        for dict_item in list(dict_data):
            pass

    except ObjectDoesNotExist:
        return response_failure(10023, '查询对象结果为空')
    return response_success(data=list(dict_data))
