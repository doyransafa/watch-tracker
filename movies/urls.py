from django.urls import path
from .views import first_view, search, movie_details, tv_details, person_details, season_details, toggle_event, post_comment, list_comments

urlpatterns = [
    path('', first_view, name='first_view'),
    path('search/', search, name='search'),
    path('movie/<int:id>', movie_details, name='movie_details'),
    path('tv/<int:id>', tv_details, name='tv_details'),
    path('tv/<int:id>/season/<int:season>', season_details, name='season_details'),
    path('person/<int:id>', person_details, name='person_details'),
    
    # Events
    # possible types: movie, tv, list
    path('post_comment/<str:media_type>/<int:id>', post_comment, name='post_comment'),
    path('list_comments/<str:media_type>/<int:id>', list_comments, name='list_comments'),
    path('<str:event_type>/<str:media_type>/<int:id>',toggle_event, name='toggle_event'),
    
]
