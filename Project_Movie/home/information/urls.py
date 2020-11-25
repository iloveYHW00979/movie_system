from django.contrib import admin
from django.urls import path
from Project_Movie.home.information import views

urlpatterns = {
    path('information_list/', views.InformationList.as_view()),
    path('information_detail/<int:information_id>', views.InformationDetail.as_view()),
    path('information_img_list/', views.InformationImgList.as_view()),
    path('advertising/', views.AdvertisingInfor.as_view()),
    path('hot_information/', views.get_hot_information),
    path('upload_img/', views.UploadImg.as_view()),
}
