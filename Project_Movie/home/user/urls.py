from django.conf.urls import url
from django.urls import path

from Project_Movie.home.user import views

urlpatterns = [
    path('order/', views.UserOrderView.as_view(), name='order'),           # /users/order
    path('', views.UserInfoView.as_view(), name='info'),                  # /users

]