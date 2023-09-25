from django.urls import reverse_lazy
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetView
from .models import User, Follow
from movies.models import Event
from django.views.generic.edit import FormView
from django.contrib import messages
from .forms import RegistrationForm

class CustomLoginView(LoginView):
    def get_success_url(self):
        return '/'

    def form_valid(self, form):
        messages.success(self.request, "You have been successfully logged in.")
        return super().form_valid(form)


class RegistrationView(FormView):
    model = User
    template_name = 'registration/register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)

def profile_view(request, username):

    user = User.objects.get(username=username)
    followers = Follow.objects.filter(following=user)
    following = Follow.objects.filter(follower=user)
    likes = Event.objects.filter(user=user, type='like')
    bookmarks = Event.objects.filter(user=user, type='bookmark')
    watched = Event.objects.filter(user=user, type='watched')
    ratings = Event.objects.filter(user=user, type='rating')

    context = {
        'profile': username,
        'followers' : followers,
        'following' : following,
        'likes' : {
            'all' : likes,
            'movies' : likes.exclude(movie__isnull=True),
            'tv_series': likes.exclude(tv_series__isnull=True,).exclude(tv_episode__isnull=False),
            'tv_episodes': likes.exclude(tv_episode__isnull=True),
        },
        'bookmarks': {
            'all': bookmarks,
            'movies': bookmarks.exclude(movie__isnull=True),
            'tv_series': bookmarks.exclude(tv_series__isnull=True,).exclude(tv_episode__isnull=False),
            'tv_episodes': bookmarks.exclude(tv_episode__isnull=True),
        },
        'watched': {
            'all': watched,
            'movies': watched.exclude(movie__isnull=True),
            'tv_series': watched.exclude(tv_series__isnull=True,).exclude(tv_episode__isnull=False),
            'tv_episodes': watched.exclude(tv_episode__isnull=True),
        },
        'ratings': {
            'all': ratings,
            'movies': ratings.exclude(movie__isnull=True),
            'tv_series': ratings.exclude(tv_series__isnull=True,).exclude(tv_episode__isnull=False),
            'tv_episodes': ratings.exclude(tv_episode__isnull=True),
        },
    }

    return render(request, 'profile.html', context)

def follow_unfollow(request, username):

    own_user = request.user
    try:
        target_user = User.objects.get(username=username)
    except User.DoesNotExist:
        return HttpResponse('No such user!!!')

    if own_user == target_user:
        return HttpResponse('You cannot follow yourself!!!')


    follow, created = Follow.objects.get_or_create(follower=own_user, following=target_user)

    if created:
        return HttpResponse('Followed')
    else:
        follow.delete()
        return HttpResponse('Unfollowed')

