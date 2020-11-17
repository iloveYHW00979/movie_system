from django.conf.urls import url
from django.urls import path

from Project_Movie.home.user import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('order/', views.UserOrderView.as_view(), name='order'),           # /users/order
    path('', views.UserInfoView.as_view(), name='info'),                  # /users

]