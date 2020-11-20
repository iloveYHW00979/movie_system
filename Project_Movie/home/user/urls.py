from django.conf.urls import url
from django.urls import path

from Project_Movie.home.user import views

urlpatterns = [
    path('', views.UserInfoView.as_view()),          # /users
    path('comment/', views.UserCommentView.as_view()),
    path('purse/', views.UserPurseView.as_view()),
    path('collect/', views.UserCollectView.as_view())

]