from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    watchlist = models.ManyToManyField('Auction', related_name='watchlist', blank=True)
    def __str__(self):
        return f"{self.username}"
    pass

class Auction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField( max_length=1024, default=None)
    description = models.TextField()
    startPrice = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    currentPrice = models.DecimalField(max_digits=12, decimal_places=2,default=0)
    imageURL = models.URLField(default=None)
    createdOn = models.DateTimeField(auto_now_add=True)
    isActive = models.BooleanField(default=True)
    category = models.CharField(max_length=64, blank=True)
    winner = models.CharField(max_length=64, blank=True)
    def __str__(self):
        return f"{self.user} - {self.id} - {self.title}"
    
class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bidAmount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    bidDate = models.DateTimeField(auto_now_add=True)
    listing = models.ForeignKey(Auction, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.user} bid ${self.bidAmount}"
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    commentText = models.TextField()
    datePosted = models.DateTimeField(auto_now_add=True)
    listing = models.ForeignKey(Auction, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.user} commented {self.commentText}"



   
