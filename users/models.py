from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        Profile.objects.get_or_create(user=self)

    def __str__(self):
        return self.username
    
    @property
    def notification_group_name(self):
        return f'user_{self.id}'
    


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(null=True)

    def __str__(self):
        return self.user.username


class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    created_at = models.DateField(auto_now_add=True)



    def __str__(self) -> str:
        return f'{self.follower.username} followed {self.following.username}'

