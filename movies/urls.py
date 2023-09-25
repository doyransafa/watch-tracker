from django.urls import path
from .views import home, search, movie_details, tv_details, person_details, season_details, toggle_event, post_comment, list_comments, bulk_watched

urlpatterns = [
    path('', home, name='home'),
    path('search/', search, name='search'),
    path('movie/<int:id>', movie_details, name='movie_details'),
    path('tv/<int:id>', tv_details, name='tv_details'),
    path('tv/<int:id>/season/<int:season>', season_details, name='season_details'),
    path('person/<int:id>', person_details, name='person_details'),
    
    path('post_comment/<str:media_type>/<int:id>', post_comment, name='post_comment'),
    path('list_comments/<str:media_type>/<int:id>', list_comments, name='list_comments'),
    path('<str:event_type>/<str:media_type>/<int:id>',toggle_event, name='toggle_event'),
    
    path('bulk_watched/<int:id>', bulk_watched, name='bulk_watched'),
]


