from Project_Movie.home.cinema.models import Cinema, Viewing, Order, Seat
from Project_Movie.home.movies.models import Movies, SysDictData, Cast, MovieImages, Comment
from Project_Movie.home.information.models import InformationManage
from rest_framework import serializers

from Project_Movie.home.user.models import User


class CinemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cinema
        fields = "__all__"


class ViewingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Viewing
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = "__all__"


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
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    movie_release_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

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
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

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

    class Meta:
        model = InformationManage
        fields = "__all__"
