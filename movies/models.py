from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

class User(AbstractUser):
    pass

class Movie(models.Model):

    tmdb_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=250)

    def __str__(self) -> str:
        return f'{self.name}'

class Tv_Series(models.Model):

    tmdb_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=250)

    def __str__(self) -> str:
        return f'{self.name}'

class Tv_Episode(models.Model):

    tv_series = models.ForeignKey(Tv_Series, on_delete=models.CASCADE)
    season = models.IntegerField()
    episode = models.IntegerField()

    def __str__(self) -> str:
        return f'{self.tv_series.name} - Season {self.season}, Episode {self.episode}'
    
class List(models.Model):

    tmdb_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=250)


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
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)], default=0)

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