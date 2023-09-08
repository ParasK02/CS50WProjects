from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followers = models.ManyToManyField("self", symmetrical=False, related_name="following")
    def get_followers(self):
        return self.followers.all()

    def get_following(self):
        return self.following.all()

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "followers": [follower.username for follower in self.get_followers()],
            "following": [followed.username for followed in self.get_following()],
        }
    pass

class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="posts")
    text = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveIntegerField(default=0)
    liked_by = models.ManyToManyField(User, through='Like', related_name='liked_posts')
    def likes_count(self):
        return self.liked_by.count()
    
    def serialize(self):
        return{
            "id": self.id,
            "user": self.user.serialize(),
            "text": self.text,
            "timestamp": self.timestamp,
            "likes": self.likes,
            

        }
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    liked_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        unique_together = ('user', 'post')