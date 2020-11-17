from django.http import HttpResponse, JsonResponse
import json
from Project_Movie.Util.utils import response_success, response_failure, paginate_success
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from Project_Movie.home.movies.models import Movies, SysDictData, Cast, \
    MovieImages, Comment
from Project_Movie.Util.serializers import MoviesSerializer, \
    SysDataSerializer, CastSerializer, CommentSerializer, MovieImagesSerializer

from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination


# class CustomPageNumberPagination(PageNumberPagination):
#     page_size = 10
# page_size_query_param = 'size'
# max_page_size = 10


class MovieList(APIView):
    """
    列出所有的movies或者创建一个新的movie。
    """

    def get(self, request):
        movie_type = request.GET.get('movie_type')  # 类型
        movie_region = request.GET.get('movie_region')  # 区域
        movie_era = request.GET.get('movie_era')  # 年代
        movie_status = request.GET.get('movie_status')  # 状态
        movie_sort = request.GET.get('movie_sort')  # 排序 0:按热门排序/1：按时间排序/2：按评价排序
        movie_sort = movie_sort if movie_sort is not None else 1
        sort_list = ['-sort_hot', '-movie_release_date', '-movie_score']
        kwargs = {}

        if movie_type is not None:
            kwargs['movie_type'] = movie_type
        if movie_region is not None:
            kwargs['movie_region'] = movie_region
        if movie_era is not None:
            kwargs['movie_era'] = movie_era
        if movie_status is not None:
            kwargs['movie_status'] = movie_status

        movies = Movies.objects.filter(**kwargs).all().order_by(sort_list[movie_sort])
        total = movies.count()

        pg = PageNumberPagination()  # 创建分页对象
        page_movies = pg.paginate_queryset(queryset=movies, request=request, view=self)  # 获取分页的数据
        serializer = MoviesSerializer(page_movies, many=True)
        return paginate_success(code=200, data=serializer.data, total=total)

    def post(self, request):
        movie_name = request.data.get('movie_name')
        movie = Movies.objects.filter(movie_name=movie_name)
        if movie:
            return response_failure(code=500, message='数据已存在')
        else:
            serializer = MoviesSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return response_success(code=201)
            return response_failure(code=400)


class MovieDetail(APIView):
    """
    检索，更新或删除一个movie示例。
    """

    def get(self, request, movie_id):
        try:
            movie = Movies.objects.get(id=movie_id)
            serializer = MoviesSerializer(movie)
        except Movies.DoesNotExist:
            return response_failure(code=404)
        return response_success(code=200, data=serializer.data)

    def put(self, request, movie_id):
        try:
            movie = Movies.objects.get(id=movie_id)
            serializer = MoviesSerializer(movie, data=request.data)
        except Movies.DoesNotExist:
            return response_failure(code=404)

        if serializer.is_valid():
            serializer.save()
            return response_success(code=200, data=serializer.data)
        return response_failure(code=400)

    def delete(self, request, movie_id):
        try:
            movie = Movies.objects.get(id=movie_id)
            movie.delete()
        except Movies.DoesNotExist:
            return response_failure(code=404)
        return response_success(code=200)


class SysDict(APIView):
    """
    电影首页基础数据
    :param request:
    :return: 电影状态/电影类型/电影区域/电影年代/演职人员类型
    """

    def get(self, request):
        type_list = ['movie_status', 'movie_type', 'movie_region', 'movie_era', 'cast_type']
        try:
            dict_data = SysDictData.objects.filter(dict_type__in=type_list, status=0).order_by('dict_sort') \
                .all()
            serializer = SysDataSerializer(dict_data, many=True)
            movie_status_list = [element for element in serializer.data if element['dict_type'] == 'movie_status']
            movie_type_list = [element for element in serializer.data if element['dict_type'] == 'movie_type']
            movie_region_list = [element for element in serializer.data if element['dict_type'] == 'movie_region']
            movie_era_list = [element for element in serializer.data if element['dict_type'] == 'movie_era']
            cast_type_list = [element for element in serializer.data if element['dict_type'] == 'cast_type']
            result_list = {
                'movie_status_list': movie_status_list,
                'movie_type_list': movie_type_list,
                'movie_region_list': movie_region_list,
                'movie_era_list': movie_era_list,
                'cast_type_list': cast_type_list
            }
        except ObjectDoesNotExist:
            return response_failure(code=404)
        return response_success(code=200, data=result_list)


class CastList(APIView):
    """
    根据movie_id检索人员或者创建一个新的人员。
    根据cast_id修改或者删除人员。
    """

    def get(self, request):
        movie_id = request.GET.get('movie_id')
        if movie_id is None:
            return response_failure(code=400)
        try:
            cast = Cast.objects.filter(movie_id=movie_id).all()
            serializer = CastSerializer(cast, many=True)
        except Cast.DoesNotExist:
            return response_failure(code=404)
        return response_success(code=200, data=serializer.data)

    def put(self, request):
        cast_id = request.data.get('cast_id')
        if cast_id is None:
            return response_failure(code=400)
        try:
            cast = Cast.objects.get(id=cast_id)
            serializer = CastSerializer(cast, data=request.data)
        except Cast.DoesNotExist:
            return response_failure(code=404)

        if serializer.is_valid():
            serializer.save()
            return response_success(code=200, data=serializer.data)
        return response_failure(code=400)

    def delete(self, request):
        cast_id = request.data.get('cast_id')
        if cast_id is None:
            return response_failure(code=400)
        try:
            cast = Cast.objects.get(id=cast_id)
            cast.delete()
        except Cast.DoesNotExist:
            return response_failure(code=404)
        return response_success(code=200)

    def post(self, request):
        serializer = CastSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response_success(code=201)
        return response_failure(code=400)


class CommentList(APIView):
    """
    根据movie_id检索评论或者创建一个新的评论。
    根据comment_id修改或者删除评论。
    """

    def get(self, request):
        movie_id = request.GET.get('movie_id')
        if movie_id is None:
            return response_failure(code=400)
        try:
            comment = Comment.objects.filter(movie_id=movie_id).all()
            serializer = CommentSerializer(comment, many=True)
        except Comment.DoesNotExist:
            return response_failure(code=404)
        return response_success(code=200, data=serializer.data)

    def put(self, request):
        comment_id = request.data.get('comment_id')
        if comment_id is None:
            return response_failure(code=400)
        try:
            comment = Comment.objects.get(id=comment_id)
            serializer = CommentSerializer(comment, data=request.data)
        except Comment.DoesNotExist:
            return response_failure(code=404)

        if serializer.is_valid():
            serializer.save()
            return response_success(code=200, data=serializer.data)
        return response_failure(code=400)

    def delete(self, request):
        comment_id = request.data.get('comment_id')
        if comment_id is None:
            return response_failure(code=400)
        try:
            comment = Comment.objects.get(id=comment_id)
            comment.delete()
        except Comment.DoesNotExist:
            return response_failure(code=404)
        return response_success(code=200)

    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response_success(code=201)
        return response_failure(code=400)


class MovieImagesList(APIView):
    """
    根据movie_id检索图集或者创建一个新的图集。
    根据image_id修改或者删除图集。
    """

    def get(self, request):
        movie_id = request.GET.get('movie_id')
        if movie_id is None:
            return response_failure(code=400)
        try:
            image = MovieImages.objects.filter(movie_id=movie_id).all()
            serializer = MovieImagesSerializer(image, many=True)
        except MovieImages.DoesNotExist:
            return response_failure(code=404)
        return response_success(code=200, data=serializer.data)

    def put(self, request):
        image_id = request.data.get('image_id')
        if image_id is None:
            return response_failure(code=400)
        try:
            image = MovieImages.objects.get(id=image_id)
            serializer = MovieImagesSerializer(image, data=request.data)
        except MovieImages.DoesNotExist:
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
            image = MovieImages.objects.get(id=image_id)
            image.delete()
        except MovieImages.DoesNotExist:
            return response_failure(code=404)
        return response_success(code=200)

    def post(self, request):
        serializer = MovieImagesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response_success(code=201)
        return response_failure(code=400)