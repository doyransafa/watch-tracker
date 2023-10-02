from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import User


class List(models.Model):

    name = models.CharField(max_length=250)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(max_length=2500, null=True)
    public = models.CharField(max_length=20, choices=[(
        'public', 'Public, anyone can see'), ('friends_only', 'Friends Only'), ('private', 'Private')])

    def __str__(self) -> str:
        return f'{self.name} by {self.user.username}'


class Movie(models.Model):

    tmdb_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=250)
    poster_id = models.CharField(max_length=250, null=True, default=None)
    list = models.ManyToManyField(List, related_name='movies')

    def __str__(self) -> str:
        return f'{self.name}'


class Tv_Series(models.Model):

    tmdb_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=250)
    poster_id = models.CharField(max_length=250, null=True, default=None)
    list = models.ManyToManyField(List, related_name='tv_series')

    def __str__(self) -> str:
        return f'{self.name}'


class ListItem(models.Model):

    list = models.ForeignKey(List, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, null=True)
    tv_series = models.ForeignKey(Tv_Series, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self) -> str:
        if self.movie != None:
            return f'{self.movie.name} added to the list {self.list.name} by {self.list.user.username}'
        if self.tv_series != None:
            return f'{self.tv_series.name} added to the list {self.list.name} by {self.list.user.username}'


class Tv_Episode(models.Model):

    tv_series = models.ForeignKey(Tv_Series, on_delete=models.CASCADE)
    season = models.IntegerField()
    episode = models.IntegerField()

    def __str__(self) -> str:
        return f'{self.tv_series.name} - Season {self.season}, Episode {self.episode}'


class Event(models.Model):

    TYPE_OPTIONS = [('like', 'liked'), ('watched', 'watched'),
                    ('watchlist', 'Added to Watchlist'), ('comment', 'Commented'), ('list', 'Created a List'), ('rating', 'Rated')]

    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=TYPE_OPTIONS)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, null=True)
    tv_series = models.ForeignKey(Tv_Series, on_delete=models.CASCADE, null=True)
    tv_episode = models.ForeignKey(Tv_Episode, on_delete=models.CASCADE, null=True)
    list = models.ForeignKey(List, on_delete=models.CASCADE, null=True)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], default=0)

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        if self.movie:
            return f'{self.user.username} - {self.type} - {self.movie.name} on {self.created_at}'
        elif self.tv_series:
            return f'{self.user.username} - {self.type} - {self.tv_series.name} on {self.created_at}'
    

class Comment(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, null=True)
    tv_series = models.ForeignKey(Tv_Series, on_delete=models.CASCADE, null=True)
    tv_episode = models.ForeignKey(Tv_Episode, on_delete=models.CASCADE, null=True)
    list = models.ForeignKey(List, on_delete=models.CASCADE, null=True)
    comment = models.TextField(max_length=5000)
