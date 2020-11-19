from django.contrib import admin
from django.urls import path
from Project_Movie.home.movies import views

urlpatterns = {
    path('movie_list/', views.MovieList.as_view()),
    path('movie_detail/<int:movie_id>', views.MovieDetail.as_view()),
    path('sys_data/', views.SysDict.as_view()),
    path('cast/', views.CastList.as_view()),
    path('comment/', views.CommentList.as_view()),
    path('movie_images/', views.MovieImagesList.as_view()),
    path('rank_list/', views.RankList.as_view()),
    # path('search_movie/', views.SearchMovie.as_view()),
}
