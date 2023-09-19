import requests
import json

from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q

from .models import Movie, Tv_Series, List, Event, Tv_Episode, Comment

HEADERS = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyODIxNzQ2NTU4YTY1YTNlMTViMTExNTEzMGVkNjRiOCIsInN1YiI6IjY0ZmM4NmQzZWZlYTdhMDBjMzk0YzZmNCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.CACTdfj6jXGcaHyFKzPBasNGgrNIMLLn1MUDm9Aoc28"
}


def first_view(request):

    return render(request, 'home.html', {'hello': 'hello'})


def search(request):

    search_text = request.GET.get('search', '')
    option = request.GET.get('type', 'multi')

    url = f"https://api.themoviedb.org/3/search/{option}?query={search_text}&include_adult=false&page=1&api_key=2821746558a65a3e15b1115130ed64b8"

    results = requests.get(url, headers=HEADERS).json()

    context = {'results': results, 'type': option}

    print(url)

    return render(request, 'search_results.html', context)


def movie_details(request, id):

    appends = 'credits,watch/providers'
    url = f"https://api.themoviedb.org/3/movie/{id}?append_to_response={appends}"

    results = requests.get(url, headers=HEADERS).json()
    json_string = json.dumps(results)
    clean_json_string = json_string.replace(
        'watch/providers', 'watch_providers')

    json_data = json.loads(clean_json_string)
    
    related_events = Event.objects.filter(
        Q(user=request.user), Q(movie__tmdb_id=id))

    liked = True if related_events.filter(Q(type='like')).exists() else False
    bookmarked = True if related_events.filter(Q(type='bookmark')).exists() else False
    watched = True if related_events.filter(Q(type='watched')).exists() else False
    try:
        rating = related_events.filter(Q(type='rating'))[0].rating
    except IndexError:
        rating = 0

    user_relation = {
        'bookmarked': bookmarked,
        'liked': liked,
        'watched': watched,
        'rating' : rating
    }

    context = {'movie': json_data, 'user_relation': user_relation}

    return render(request, 'movie_details.html', context)


def tv_details(request, id):

    appends = 'external_ids,watch/providers,aggregate_credits,similar,recommendations'
    url = f"https://api.themoviedb.org/3/tv/{id}?append_to_response={appends}"

    results = requests.get(url, headers=HEADERS).json()
    json_string = json.dumps(results)
    clean_json_string = json_string.replace(
        'watch/providers', 'watch_providers')

    json_data = json.loads(clean_json_string)

    related_events = Event.objects.filter(Q(user=request.user),Q(tv_series__tmdb_id=id))

    liked = True if related_events.filter(Q(type='like')).exists() else False
    bookmarked = True if related_events.filter(Q(type='bookmark')).exists() else False
    watched = True if related_events.filter(Q(type='watched')).exists() else False
    try:
        rating = related_events.filter(Q(type='rating'))[0].rating
    except IndexError:
        rating = 0

    user_relation = {
        'liked': liked,
        'watched': watched,
        'bookmarked': bookmarked,
        'rating' : rating
    }

    context = {'tv': json_data, 'user_relation': user_relation}

    return render(request, 'tv_details.html', context)


def season_details(request, id, season):

    url = f"https://api.themoviedb.org/3/tv/{id}?append_to_response=season/{season}"

    results = requests.get(url, headers=HEADERS).json()
    json_string = json.dumps(results)
    clean_json_string = json_string.replace(
        f'season/{season}', 'episodes')

    json_data = json.loads(clean_json_string)

    try:
        tv_series = Tv_Series.objects.get(tmdb_id=id)
    except Tv_Series.DoesNotExist:
        tv_series = None

    for episode in json_data['episodes']['episodes']:

        related_events = Event.objects.filter(
            Q(user=request.user),
            Q(tv_episode__tv_series=tv_series, tv_episode__season=season,tv_episode__episode=episode['episode_number']))

        episode['liked'] = True if related_events.filter(Q(type='like')).exists() else False
        episode['watched'] = True if related_events.filter(Q(type='watched')).exists() else False
        try:
            episode['rating'] = related_events.filter(Q(type='rating'))[0].rating
        except IndexError:
            episode['rating'] = 0

    context = {"season": json_data["episodes"], 'name': json_data['name']}

    return render(request, 'season_details.html', context)


def person_details(request, id):

    language = 'en-US'
    appends = 'movie_credits,tv_credits'
    url = f"https://api.themoviedb.org/3/person/{id}?language={language}&append_to_response={appends}"

    results = requests.get(url, headers=HEADERS).json()

    cinema_roles = [role['department']
                    for role in results.get('movie_credits', []).get('crew', [])]

    is_cinema_actor = len(results.get('movie_credits', []).get('cast', []))
    is_cinema_director = True if 'Directing' in cinema_roles else False
    is_cinema_producer = True if 'Production' in cinema_roles else False
    is_cinema_writer = True if 'Writing' in cinema_roles else False

    tv_roles = [role['department']
                for role in results.get('tv_credits', []).get('crew', [])]

    is_tv_actor = len(results.get('movie_credits', []).get('cast', []))
    is_tv_director = True if 'Directing' in tv_roles else False
    is_tv_producer = True if 'Production' in tv_roles else False
    is_tv_writer = True if 'Writing' in tv_roles else False
    is_tv_creator = True if 'Creator' in tv_roles else False

    roles = {
        'is_cinema_related': any([is_cinema_actor, is_cinema_director, is_cinema_director, is_cinema_producer]),
        'is_cinema_actor': is_cinema_actor,
        'is_cinema_director': is_cinema_director,
        'is_cinema_producer': is_cinema_producer,
        'is_cinema_writer': is_cinema_writer,
        'is_tv_related': any([is_tv_actor, is_tv_director, is_tv_director, is_tv_producer, is_tv_creator]),
        'is_tv_actor': is_tv_actor,
        'is_tv_creator': is_tv_creator,
        'is_tv_director': is_tv_director,
        'is_tv_producer': is_tv_producer,
        'is_tv_writer': is_tv_writer,
    }

    context = {'person': results, 'roles': roles}

    return render(request, 'person_details.html', context)


def toggle_event(request, event_type, media_type, id):

    name = request.GET.get('name', '')
    try:
        season = int(request.GET.get('season', 0))
        episode = int(request.GET.get('episode', 0))
        rating = int(request.GET.get('rating', 0) )
    except ValueError:
        pass

    user = request.user
    type = event_type
    movie, tv_series, list, tv_episode = None, None, None, None
    if media_type == 'movie':
        movie, _ = Movie.objects.get_or_create(tmdb_id=id, name=name)
    elif media_type == 'tv':
        tv_series, _ = Tv_Series.objects.get_or_create(tmdb_id=id, name=name)
    elif media_type == 'episode':
        tv_series, _ = Tv_Series.objects.get_or_create(tmdb_id=id, name=name)
        tv_episode, _ = Tv_Episode.objects.get_or_create(tv_series=tv_series, season=season, episode=episode)
    else:
        list, _ = List.objects.get_or_create(tmdb_id=id, name=name)

    event, created = Event.objects.get_or_create(user=user, type=type, movie=movie, tv_series=tv_series, tv_episode=tv_episode, list=list, rating=rating)

    if created:
        if type == 'like':
            return HttpResponse('favorite')
        elif type == 'bookmark':
            return HttpResponse('bookmark')
        elif type == 'watched':
            return HttpResponse('visibility')
        elif type == 'rating':
            return HttpResponse(f'<span class="material-icons text-yellow-500">{"star " * rating}</span>')
    else:
        if type == 'rating':
            event.rating = rating
            event.save(update_fields=['rating'])
            return HttpResponse(f'<span class="material-icons text-yellow-500">{"star " * rating}</span>')
        else:
            event.delete()
            if type == 'like':
                return HttpResponse('favorite_border')
            elif type == 'bookmark':
                return HttpResponse('bookmark_border')
            elif type == 'watched':
                return HttpResponse('visibility_off')
            

def post_comment(request, media_type, id):

    comment = request.POST.get('comment')
    name = request.GET.get('name')
    user = request.user

    print(user, comment, name)

    movie, tv_series, list = None, None, None
    if media_type == 'movie':
        movie, _ = Movie.objects.get_or_create(tmdb_id=id, name=name)
    elif media_type == 'tv':
        tv_series, _ = Tv_Series.objects.get_or_create(tmdb_id=id, name=name)
    elif media_type == 'list':
        list, _ = List.objects.get_or_create(tmdb_id=id, name=name)
    else:
        raise HttpResponse(404)
    
    

    comment_object = Comment.objects.create(user=user, movie=movie, tv_series=tv_series, list=list, comment=comment)

    return HttpResponse(f'{comment} - {user.username} - {comment_object.created_at}')


def list_comments(request, media_type, id):

    user = request.user
    page = int(request.GET.get('page', 1))
    pagination = 5

    movie, tv_series, list = None, None, None
    if media_type == 'movie':
        try:
            movie= Movie.objects.get(tmdb_id=id)
        except Movie.DoesNotExist:
            pass
    elif media_type == 'tv':
        try:
            tv_series= Tv_Series.objects.get(tmdb_id=id)
        except Tv_Series.DoesNotExist:
            pass
    elif media_type == 'list':
        try:
            list= List.objects.get(tmdb_id=id)
        except List.DoesNotExist:
            pass
    else:
        raise HttpResponse(404)

    post_comments = Comment.objects.filter(movie=movie, tv_series=tv_series, list=list)
    comment_count = post_comments.count()
    total_pages = (comment_count // pagination) + 1

    print(post_comments, comment_count, total_pages, page)
    
    if comment_count >= page * pagination:
        post_comments = post_comments[comment_count - (page * pagination):]

    details = {
        'total_pages': total_pages, 
        'current_page': page,
        'next_page': page + 1 if page != total_pages else total_pages,
        'type' : media_type,
        'id' : id,
    }
        

    context = {'comments': post_comments, 'details': details }

    return render(request, 'partials/comment_list.html', context)