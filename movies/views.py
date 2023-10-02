import requests
import json

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Q

from .models import Movie, Tv_Series, List, Event, Tv_Episode, Comment, ListItem
from users.models import Follow
from .forms import CreateListForm, UpdateListForm

HEADERS = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyODIxNzQ2NTU4YTY1YTNlMTViMTExNTEzMGVkNjRiOCIsInN1YiI6IjY0ZmM4NmQzZWZlYTdhMDBjMzk0YzZmNCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.CACTdfj6jXGcaHyFKzPBasNGgrNIMLLn1MUDm9Aoc28"
}


def home(request):

    return render(request, 'index.html')


def search(request):

    search_text = request.GET.get('search', '')
    option = request.GET.get('type', 'multi')

    url = f"https://api.themoviedb.org/3/search/{option}?query={search_text}&include_adult=false&page=1"

    results = requests.get(url, headers=HEADERS).json()

    context = {'results': results, 'type': option}

    return render(request, 'partials/overall_search_results.html', context)


def list_add_search(request):

    search_text = request.GET.get('search', '')
    list_id = int(request.GET.get('list_id', 0))

    url = f"https://api.themoviedb.org/3/search/multi?query={search_text}&include_adult=false&page=1"

    results = requests.get(url, headers=HEADERS).json()

    results = [result for result in results['results'] if result['media_type'] != 'person']

    context = {'results': results, 'list_id': list_id}

    return render(request, 'partials/list_search_results.html', context)


def movie_details(request, id):

    appends = 'credits,watch/providers,recommendations'
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

    related_events = Event.objects.filter(Q(user=request.user), Q(
        tv_series__tmdb_id=id), Q(tv_episode__isnull=True))

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

    user_lists = List.objects.filter(user=request.user)

    try:
        tv_series = Tv_Series.objects.get(tmdb_id=id)
        list_items_object = ListItem.objects.filter(tv_series=tv_series).filter(list__user=request.user)
        list_items_dict = {item.list.id:item.id for item in list_items_object}

    except:
        tv_series = None
        list_items_dict = {}


    context = {'tv': json_data, 'user_relation': user_relation, 'user_lists': user_lists, 'list_items': list_items_dict}

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

    context = {"season": json_data["episodes"], 
               'name': json_data['name'],
               'poster_id': json_data['poster_path'], 
               'show_id': json_data['id'],
               'first_season': json_data['seasons'][0]['season_number'],
               'last_season': json_data['seasons'][-1]['season_number']}

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
    poster_id = request.GET.get('poster_id')
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
        movie, _ = Movie.objects.get_or_create(
            tmdb_id=id, name=name, poster_id=poster_id)
    elif media_type == 'tv':
        tv_series, _ = Tv_Series.objects.get_or_create(tmdb_id=id, name=name, poster_id=poster_id)
    elif media_type == 'episode':
        tv_series, _ = Tv_Series.objects.get_or_create(tmdb_id=id, name=name, poster_id=poster_id)
        tv_episode, _ = Tv_Episode.objects.get_or_create(tv_series=tv_series, season=season, episode=episode)
    elif media_type == 'list':
        list, _ = List.objects.get_or_create(tmdb_id=id, name=name)

    event, created = Event.objects.get_or_create(user=user, type=type, movie=movie, tv_series=tv_series, tv_episode=tv_episode, list=list, rating=rating)

    params = {
        'rating': rating,
        'event_type': event_type,
        'media_type': media_type,
        'id': id,
        'name': name,
        'poster_id': poster_id,
        'season': season,
        'episode': episode,
    }

    if created:
        if type == 'like':
            response = HttpResponse('favorite')
            message_body = f'{name} is marked as watched!' if media_type != 'episode' else f'{name} - Season {season} - Episode {episode} is liked!'
        elif type == 'bookmark':
            response = HttpResponse('bookmark')
            message_body =f'{name} is bookmarked!'
        elif type == 'watched':
            response = HttpResponse('visibility')
            message_body = f'{name} is marked as watched!' if media_type != 'episode' else f'{name} - Season {season} - Episode {episode} is marked as watched!'
        elif type == 'rating':
            response = render(request, 'partials/rating.html', params)
            message_body = f'{name} is rated {rating} stars!' if media_type != 'episode' else f'{name} - Season {season} - Episode {episode} is is rated {rating} stars!'
        
        response['HX-Trigger'] = json.dumps({
            'messageCreated': {
                'message_body': message_body
            }
        })
        return response
    else:
        event.delete()
        if type == 'like':
            response = HttpResponse('favorite_border')
            message_body = f'{name} is removed from liked!' if media_type != 'episode' else f'{name} - Season {season} - Episode {episode} is removed from liked!'
        elif type == 'bookmark':
            response = HttpResponse('bookmark_border')
            message_body = f'{name} is removed from bookmarks!'
        elif type == 'watched':
            response = HttpResponse('visibility_off')
            message_body = f'{name} is removed from watched!' if media_type != 'episode' else f'{name} - Season {season} - Episode {episode} is removed from watched!'
        elif type == 'rating':
            response = render(request, 'partials/rating_select.html', params)
            message_body = f'{name} is removed from watched!' if media_type != 'episode' else f'{name} - Season {season} - Episode {episode}\'s rating is removed!'
        
        response['HX-Trigger'] = json.dumps({
            'messageCreated': {
                'message_body': message_body,
            }
        })
        
        return response


def post_comment(request, media_type, id):

    comment = request.POST.get('comment')
    name = request.GET.get('name')
    user = request.user

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

    page = int(request.GET.get('page', 1))
    pagination = 10

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


def bulk_watched(request, id):

    season = request.GET.get('season', 'all')
    name = request.GET.get('name', '')
    poster_id = request.GET.get('poster_id')
    tv_series, _ = Tv_Series.objects.get_or_create(tmdb_id=id, name=name, poster_id=poster_id)

    if season != 'all':
        loop_over = [int(season)]
    else:
        last_season = int(request.GET.get('last_season'))
        loop_over = range(1,last_season+1)

    for season in loop_over:
        season = int(season)
        url = f"https://api.themoviedb.org/3/tv/{id}?append_to_response=season/{season}"

        results = requests.get(url, headers=HEADERS).json()
        json_string = json.dumps(results)
        clean_json_string = json_string.replace(f'season/{season}', 'episodes')

        json_data = json.loads(clean_json_string)

        for index, episode in enumerate(json_data['episodes']['episodes'], 1):
            tv_episode, _ = Tv_Episode.objects.get_or_create(tv_series=tv_series, season=season, episode=index)
            Event.objects.get_or_create(user=request.user, type='watched', tv_series=tv_series, tv_episode=tv_episode)

    print('Done')
    return HttpResponse('visibility')


def create_list(request):
    
    if request.method == 'POST':
        form = CreateListForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            new_list = form.save()
            return redirect('list_details', id=new_list.id)
    else:
        form = CreateListForm()

    return render(request, 'list_create.html', {'form':form})


def list_details(request, id):
    list = List.objects.get(id=id)

    list_items = ListItem.objects.filter(list=list)

    context = {'list': list, 'list_items': list_items}

    return render(request, 'list_details.html', context)


def update_list_details(request, id):
    
    list = get_object_or_404(List, id=id)

    if request.method == 'POST':
        form = UpdateListForm(request.POST, instance=list)
        if form.is_valid():
            form.save()

            return redirect('list_details', id=id)
    else:
        form = UpdateListForm(instance=list)
    
    return render(request, 'list_update.html', {'form': form, 'list': list})


def delete_list(request, id):
    
    list = List.objects.get(id=id)

    list.delete()

    return redirect('profile_view', username=request.user.username)


def add_items_to_list(request, id):

    list = List.objects.get(id=id)
    media_type = request.GET.get('media_type')
    media_id = request.GET.get('media_id')
    name = request.GET.get('name')
    poster_id = request.GET.get('poster_id')
    all_items = ListItem.objects.filter(list=list)

    if media_type == 'movie':
        movie, _ = Movie.objects.get_or_create(tmdb_id=media_id, name=name, poster_id=poster_id)
        tv_series = None
    elif media_type == 'tv':
        tv_series, _ = Tv_Series.objects.get_or_create(tmdb_id=media_id, name=name, poster_id=poster_id)
        movie = None

    _, created = ListItem.objects.get_or_create(list=list, movie=movie, tv_series=tv_series)

    if created:
        response = render(request, 'partials/list_items.html',{'list_items': all_items})
        message_body = f'{name} is added to the list {list.name}'
    else:
        response = render(request, 'partials/list_items.html', {'list_items': all_items})
        message_body = f'{name} is already on the list {list.name}!'

    response['HX-Trigger'] = json.dumps({
        'messageCreated': {
            'message_body': message_body,
        }, 
        'listItemAdded' : True
    })
    return response


def delete_items_from_list(request, item_id, list_id):
    list = get_object_or_404(List, id=list_id)
    list_item = get_object_or_404(ListItem, id=item_id)
    try:
        name = list_item.movie.name
    except:
        name = list_item.tv_series.name

    list_item.delete()

    all_items = ListItem.objects.filter(list=list)

    response = render(request, 'partials/list_items.html', {'list_items':all_items})
    response['HX-Trigger'] = json.dumps({
        'messageCreated': {
            'body': f'You have deleted {name} from the list',
        }
    })
    return response


def user_feed(request):

    current_page = int(request.GET.get('page', 1))
    pagination = 30

    following_users = Follow.objects.filter(follower=request.user).values_list('following', flat=True)
    # Exclude episodes to reduce bloating .exclude(tv_episode__isnull=False)
    user_feed_events = Event.objects.filter(user__in=following_users)

    event_count = user_feed_events.count()
    total_pages = (event_count // pagination) + 1

    user_feed_events = user_feed_events[(
        current_page - 1) * pagination: (pagination * current_page)]

    print(event_count, total_pages)

    context = {
        'events': user_feed_events,
        'current_page': current_page,
        'next_page': current_page + 1,
        'last_page' : True if current_page == total_pages else False
    }

    return render(request, 'partials/feed.html', context)