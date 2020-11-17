from django.contrib import admin
from django.urls import path
from Project_Movie.home.movies import views

urlpatterns = {
    # path('', views.get_all_movies),
    # path('<int:movie_id>', views.get_movie),
    # path('create/', views.create_movie),
    path('sys_data/<str:dict_type>', views.get_sys_dict),
    path('movie_dict/', views.get_movie_dict),
    path('movies_list/', views.MoviesList.as_view()),
    path('movies_detail/<int:movie_id>', views.MovieDetail.as_view()),
}
