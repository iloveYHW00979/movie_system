from Project_Movie.home.cinema.models import Cinema, Viewing, Order, Seat
from Project_Movie.home.movies.models import Movies, SysDictData
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
    class Meta:
        model = Movies
        fields = "__all__"

class SysDataSerializer(serializers.ModelSerializer):
    """
    基础数据序列表类
    """
    class Meta:
        model = SysDictData
        fields = "__all__"