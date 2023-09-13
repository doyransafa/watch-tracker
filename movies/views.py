import requests
import json

from django.shortcuts import render
from django.http import JsonResponse

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

    context = {'movie': json_data}

    return render(request, 'movie_details.html', context)


def tv_details(request, id):

    appends = 'external_ids,watch/providers,aggregate_credits,similar,recommendations'
    url = f"https://api.themoviedb.org/3/tv/{id}?append_to_response={appends}"

    results = requests.get(url, headers=HEADERS).json()
    json_string = json.dumps(results)
    clean_json_string = json_string.replace(
        'watch/providers', 'watch_providers')

    json_data = json.loads(clean_json_string)

    context = {'tv': json_data}

    return render(request, 'tv_details.html', context)


def season_details(request, id, season):

    url = f"https://api.themoviedb.org/3/tv/{id}/season/{season}"

    results = requests.get(url, headers=HEADERS).json()

    context = {"season": results}

    return render(request, 'season_details.html', context)


def person_details(request, id):

    language = 'en-US'
    appends = 'movie_credits,tv_credits'
    url = f"https://api.themoviedb.org/3/person/{id}?language={language}&append_to_response={appends}"

    results = requests.get(url, headers=HEADERS).json()

    cinema_roles = [role['department'] for role in results.get('movie_credits', []).get('crew', [])]

    is_cinema_actor = len(results.get('movie_credits', []).get('cast', []))
    is_cinema_director = True if 'Directing' in cinema_roles else False
    is_cinema_producer = True if 'Production' in cinema_roles else False
    is_cinema_writer = True if 'Writing' in cinema_roles else False

    tv_roles = [role['department'] for role in results.get('tv_credits', []).get('crew', [])]

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

    # return JsonResponse(results)

    context = {'person': results, 'roles' : roles}

    return render(request, 'person_details.html', context)
