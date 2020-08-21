from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now) # auto_now_add = True -> değiştirilemez, sabit
    # if a user gets deleted, on_delete=models.CASCADE will delete the posts related to that user
    # User -> foreign key ile baglanan table
    author = models.ForeignKey(User, on_delete=models.CASCADE) 

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"pk": self.pk}) # redirect etmek için
    