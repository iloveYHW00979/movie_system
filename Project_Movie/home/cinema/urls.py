from django.urls import path
from Project_Movie.home.cinema import views

urlpatterns = [
    path('operate/', views.CinemaView.as_view()),
    path('attribute/', views.AttributeView.as_view()),
    path('detail/', views.CinemaDetail.as_view()),
    path('view/', views.CinemaViewing.as_view()),
    path('ticket/', views.CinemaOrder.as_view()),
]
