from django.urls import path, include

urlpatterns = [
    path('cinema/', include('Project_Movie.home.cinema.urls')),
    path('movies/', include('Project_Movie.home.movies.urls')),
    path('user/', include('Project_Movie.home.user.urls'))
]
