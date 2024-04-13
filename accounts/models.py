from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):

    profile_pic = models.ImageField(upload_to="profile_pics/", blank=True)
    point = models.IntegerField(default=0)
    following = models.ManyToManyField("self", symmetrical=False, blank=True, related_name="followers")
    introduce = models.TextField(blank=True)

    def __str__(self):
        return f"{self.username} 님"
    
    def getpic(self):
        if self.profile_pic:
            return self.profile_pic.url
        return "/media/noimage.png"

    class Meta:
        pass