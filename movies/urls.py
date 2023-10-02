from django.urls import path
from .views import (home, search, movie_details, tv_details, person_details, season_details, toggle_event, 
                    post_comment, list_comments, bulk_watched, create_list, list_details, add_items_to_list, list_add_search,
                    delete_list, update_list_details, delete_items_from_list, user_feed)

urlpatterns = [
    path('', home, name='home'),
    path('feed/', user_feed, name='feed'),
    path('search/', search, name='search'),
    path('movie/<int:id>', movie_details, name='movie_details'),
    path('tv/<int:id>', tv_details, name='tv_details'),
    path('tv/<int:id>/season/<int:season>', season_details, name='season_details'),
    path('person/<int:id>', person_details, name='person_details'),
    
    ## Events
    path('post_comment/<str:media_type>/<int:id>', post_comment, name='post_comment'),
    path('list_comments/<str:media_type>/<int:id>', list_comments, name='list_comments'),
    path('toggle_event/<str:event_type>/<str:media_type>/<int:id>',toggle_event, name='toggle_event'),
    path('bulk_watched/<int:id>', bulk_watched, name='bulk_watched'),

    ## List Crud
    path('create_list', create_list, name='create_list'),
    path('delete_list/<int:id>', delete_list, name='delete_list'),
    path('update_list_details/<int:id>', update_list_details, name='update_list_details'),
    path('list_details/<int:id>', list_details, name='list_details'),
    path('add_items_to_list/<int:id>', add_items_to_list, name='add_items_to_list'),
    path('delete_items_from_list/<int:item_id>/<int:list_id>', delete_items_from_list, name='delete_items_from_list'),
    path('list_add_search', list_add_search, name='list_add_search'),
    
]


