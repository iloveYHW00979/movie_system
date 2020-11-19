from Project_Movie.home.cinema.models import Cinema, Viewing, Order, Seat
from Project_Movie.home.movies.models import Movies, SysDictData, Cast, MovieImages, Comment
from Project_Movie.home.information.models import InformationManage, InformationImg, Advertising
from rest_framework import serializers
import time

from Project_Movie.home.user.models import User


class CinemaSerializer(serializers.ModelSerializer):

    cinema_brand_lable = serializers.SerializerMethodField()
    administrative_district_lable = serializers.SerializerMethodField()
    special_hall_lable = serializers.SerializerMethodField()
    cinema_service_lable = serializers.SerializerMethodField()

    class Meta:
        model = Cinema
        fields = "__all__"

    def get_cinema_brand_lable(self, obj):
        cinema = obj
        cinema_brand = SysDictData.objects.filter(dict_code=cinema.cinema_brand)[0].dict_label
        return cinema_brand

    def get_special_hall_lable(self, obj):
        cinema = obj
        special_hall = SysDictData.objects.filter(dict_code=cinema.special_hall)[0].dict_label
        return special_hall

    def get_administrative_district_lable(self, obj):
        cinema = obj
        administrative_district = SysDictData.objects.filter(dict_code=cinema.administrative_district)[0].dict_label
        return administrative_district

    def get_cinema_service_lable(self, obj):
        cinema = obj
        cinema_service = SysDictData.objects.filter(dict_code=cinema.cinema_service)[0].dict_label
        return cinema_service


class ViewingSerializer(serializers.ModelSerializer):

    movie_info =  serializers.SerializerMethodField()
    cinema_info = serializers.SerializerMethodField()

    class Meta:
        model = Viewing
        fields = "__all__"

    def get_movie_info(self, obj):
        view = obj
        movie_id = Movies.objects.filter(id=view.movie_id)[0]
        movie_info = MoviesSerializer(movie_id).data
        return movie_info

    def get_cinema_info(self, obj):
        view = obj
        cinema_id = Cinema.objects.filter(id=view.cinema_id)[0]
        cinema_data = CinemaSerializer(cinema_id).data
        return cinema_data

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class SeatSerializer(serializers.ModelSerializer):
    view_info = serializers.SerializerMethodField()

    class Meta:
        model = Seat
        fields = "__all__"

    def get_view_info(self, obj):
        seat = obj
        view = Viewing.objects.filter(id=seat.view_id)[0]
        view_info = ViewingSerializer(view).data
        return view_info

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class MoviesSerializer(serializers.ModelSerializer):
    """
    电影序列表类
    """
    type_label = serializers.SerializerMethodField()
    region_label = serializers.SerializerMethodField()
    era_label = serializers.SerializerMethodField()
    status_label = serializers.SerializerMethodField()
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    movie_release_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    movie_hot = serializers.SerializerMethodField()

    class Meta:
        model = Movies
        fields = "__all__"

    def get_type_label(self, obj):
        movie = obj
        movie_type = SysDictData.objects.filter(dict_code=movie.movie_type)[0].dict_label
        return movie_type

    def get_region_label(self, obj):
        movie = obj
        movie_region = SysDictData.objects.filter(dict_code=movie.movie_region)[0].dict_label
        return movie_region

    def get_era_label(self, obj):
        movie = obj
        movie_era = SysDictData.objects.filter(dict_code=movie.movie_era)[0].dict_label
        return movie_era

    def get_status_label(self, obj):
        movie = obj
        movie_status = SysDictData.objects.filter(dict_code=movie.movie_status)[0].dict_label
        return movie_status

    def get_movie_hot(self, obj):
        movie = obj
        order_count = Order.objects.filter(movie_id=movie.id).count()
        return order_count


class SysDataSerializer(serializers.ModelSerializer):
    """
    基础数据序列表类
    """

    class Meta:
        model = SysDictData
        fields = "__all__"


class CastSerializer(serializers.ModelSerializer):
    """
    演职人员序列表类
    """
    type_label = serializers.SerializerMethodField()

    class Meta:
        model = Cast
        fields = "__all__"

    def get_type_label(self, obj):
        """
        获取演职人员类型
        :param obj: 当前cast的实例
        :return: 当前人员类型名称
        """
        cast = obj
        dict_label = SysDictData.objects.filter(dict_code=cast.cast_type)[0].dict_label
        return dict_label


class CommentSerializer(serializers.ModelSerializer):
    """
    评论数据序列表类
    """
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Comment
        fields = "__all__"


class MovieImagesSerializer(serializers.ModelSerializer):
    """
    图集数据序列表类
    """

    class Meta:
        model = MovieImages
        fields = "__all__"


class InformationSerializer(serializers.ModelSerializer):
    """
    资讯数据序列表类
    """
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = InformationManage
        fields = "__all__"


# class InformationImgSerializer(serializers.ModelSerializer):
#     """
#     资讯图片序列表类
#     """
#
#     class Meta:
#         model = InformationImg
#         fields = "__all__"


class AdvertisingSerializer(serializers.ModelSerializer):
    """
    首页轮播图数据序列表类
    """

    class Meta:
        model = Advertising
        fields = "__all__"