from django.db import connection
from django.http import HttpResponse, JsonResponse
import json
import re
from Project_Movie.Util.utils import response_success, response_failure, paginate_success, \
    CustomPageNumberPagination
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from Project_Movie.home.movies.models import Movies, SysDictData, Cast, \
    MovieImages, Comment, Favorite
from Project_Movie.Util.serializers import MoviesSerializer, \
    SysDataSerializer, CastSerializer, CommentSerializer, MovieImagesSerializer, \
    FavoriteSerializer

from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination


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
        movie_sort = int(movie_sort) if movie_sort is not None else 0
        key_word = request.GET.get('key_word')
        kwargs = {}

        if movie_type is not None:
            kwargs['movie_type'] = movie_type
        if movie_region is not None:
            kwargs['movie_region'] = movie_region
        if movie_era is not None:
            kwargs['movie_era'] = movie_era

        '''
        没有状态参数：根据上映时间倒序排序
        有状态参数：判断是否上映
        待上映电影根据热度和上映时间排序，热度依据为想看数
        上映电影根据热度、上映时间和评分排序，热度依据为票房
        '''
        if movie_status is not None:
            # 判断电影状态
            dict_status = SysDictData.objects.filter(dict_code=movie_status)[0].dict_sort
            if dict_status == 1:
                sort_list = ['-movie_anticipate', '-movie_release_date']
            else:
                sort_list = ['-movie_box_office', '-movie_release_date', '-movie_score']
            kwargs['movie_status'] = movie_status
        else:
            movie_sort = 0
            sort_list = ['-movie_release_date']

        if key_word is not None:
            kwargs['movie_name__contains'] = key_word
        try:
            movies = Movies.objects.filter(**kwargs).all().order_by(sort_list[movie_sort])
            total = movies.count()
            pg = CustomPageNumberPagination()  # 创建分页对象
            page_movies = pg.paginate_queryset(queryset=movies, request=request, view=self)  # 获取分页的数据
            serializer = MoviesSerializer(page_movies, many=True)
        except Movies.DoesNotExist:
            return response_failure(code=404)
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
                return response_success(code=200)
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
        key_word = request.GET.get('key_word')
        kwargs = {'movie_id': movie_id}
        if movie_id is None:
            return response_failure(code=400)
        if key_word is not None:
            kwargs['cast_name__contains'] = key_word

        try:
            cast = Cast.objects.filter(**kwargs).all()
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
            return response_success(code=200)
        return response_failure(code=400)


class CommentList(APIView):
    """
    根据movie_id检索评论或者创建一个新的评论。
    根据comment_id修改或者删除评论。
    """

    def get(self, request):
        movie_id = request.GET.get('movie_id')
        comment_type = request.GET.get('comment_type')
        if movie_id is None:
            return response_failure(code=400)
        try:
            kwargs = {"movie_id": movie_id, "comment_type": comment_type}
            comment = Comment.objects.filter(**kwargs).all()
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
            return response_success(code=200)
        return response_failure(code=400)


# def fuzzy_finder(key, data):
#     """
#     模糊查找器
#     :param key: 关键字
#     :param data: 数据
#     :return: list
#     """
#     # 结果列表
#     suggestions = []
#     # 非贪婪匹配，转换 'djm' 为 'd.*?j.*?m'
#     # pattern = '.*?'.join(key)
#     pattern = '.*%s.*'%(key)
#     # print("pattern",pattern)
#     # 编译正则表达式
#     regex = re.compile(pattern)
#     for item in data:
#         # print("item",item['name'])
#         # 检查当前项是否与regex匹配。
#         match = regex.search(item['movie_name'])
#         if match:
#             # 如果匹配，就添加到列表中
#             suggestions.append(item)
#
#     return


class AllComment(APIView):
    """
    根据movie_id检索评论或者创建一个新的评论。
    根据comment_id修改或者删除评论。
    """

    def get(self, request):
        key_word = request.GET.get('key_word')
        kwargs = {}

        if key_word is not None:
            kwargs['movie_name__contains'] = key_word

        try:
            comment = Comment.objects.filter(**kwargs).all()
            total = comment.count()

            pg = CustomPageNumberPagination()  # 创建分页对象
            page_comment = pg.paginate_queryset(queryset=comment, request=request, view=self)  # 获取分页的数据
            serializer = CommentSerializer(page_comment, many=True)

        except comment.DoesNotExist:
            return response_failure(code=404)
        return paginate_success(code=200, data=serializer.data, total=total)


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
            return response_success(code=200)
        return response_failure(code=400)


class RankList(APIView):
    """
    查询今日票房排行和最受期待排行
    """

    def get(self, request):
        try:
            # 今日票房排行
            box_office = Movies.objects.filter(movie_status=80).all() \
                             .order_by('-movie_box_office')[:10]
            box_office_serializer = MoviesSerializer(box_office, many=True)
            box_office_list = []
            for index, box_office_item in enumerate(box_office_serializer.data):
                box_office_list.append({
                    'rank': index + 1,
                    'movie_id': box_office_item['id'],
                    'movie_name': box_office_item['movie_name'],
                    'movie_box_office': box_office_item['movie_box_office'],
                })
        except Movies.DoesNotExist:
            return response_failure(code=404)

        try:
            # 最受期待排行
            anticipate = Movies.objects.filter(movie_status=81).all() \
                             .order_by('-movie_anticipate')[:10]
            anticipate_serializer = MoviesSerializer(anticipate, many=True)
            anticipate_list = []
            for index, anticipate_item in enumerate(anticipate_serializer.data):
                anticipate_list.append({
                    'rank': index + 1,
                    'movie_id': anticipate_item['id'],
                    'movie_name': anticipate_item['movie_name'],
                    'movie_anticipate': anticipate_item['movie_anticipate'],
                })
        except Movies.DoesNotExist:
            return response_failure(code=404)

        result = {
            'box_office_list': box_office_list,
            'anticipate_list': anticipate_list
        }
        return response_success(code=200, data=result)


class FavoriteOperation(APIView):
    """
    想看和取消想看操作
    """

    def delete(self, request):
        favorite_id = request.data.get('favorite_id')

        if favorite_id is None:
            return response_failure(code=400)
        try:
            favorite = Favorite.objects.get(id=favorite_id)
            favorite.delete()
        except Favorite.DoesNotExist:
            return response_failure(code=404)
        return response_success(code=200)

    def post(self, request):
        serializer = FavoriteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response_success(code=200)
        return response_failure(code=400)

    def get(self, request):
        movie_id = request.GET.get('movie_id')
        user_id = request.GET.get('user_id')
        favorite = Favorite.objects.filter(movie_id=movie_id, user_id=user_id).first()

        if favorite is None:
            return response_success(code=200)
        else:
            serializer = FavoriteSerializer(favorite)
            return response_success(code=200, data=serializer.data['id'])


class ShowingList(APIView):
    """
    热映口碑榜/国内票房榜
    """

    def get(self, request):
        select_type = request.GET.get('select_type')  # 选择类型 0：热映口碑榜/1：国内票房榜
        if select_type is None:
            return response_failure(code=400)
        try:
            movie = Movies.objects.filter(movie_status=80).all()
            if int(select_type) == 0:
                result_data = movie.order_by('-movie_score')[:10]
            elif int(select_type) == 1:
                result_data = movie.order_by('-movie_box_office')[:10]

            serializer = MoviesSerializer(result_data, many=True)
        except Movies.DoesNotExist:
            return response_failure(code=404)
        return response_success(code=200, data=serializer.data)


class AnticipateList(APIView):
    """
    最受期待榜
    """

    def get(self, request):
        try:
            anticipate = Movies.objects.filter(movie_status=81).all().order_by('-movie_anticipate')
            total = anticipate.count()

            pg = CustomPageNumberPagination()  # 创建分页对象
            page_anticipate = pg.paginate_queryset(queryset=anticipate, request=request, view=self)  # 获取分页的数据
            serializer = MoviesSerializer(page_anticipate, many=True)
        except Movies.DoesNotExist:
            return response_failure(code=404)
        return paginate_success(code=200, data=serializer.data, total=total)
