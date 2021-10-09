from django.db import models
from django.contrib.auth import get_user_model

"""
1) model for lost items/docs
2) model for found items/docs
"""


class Category(models.Model):
    category = models.SlugField(primary_key=True)


class LostItem(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='item')
    # name = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post')
    description = models.TextField(max_length=250)
    date_lost = models.DateField()
    image = models.ImageField()
    found = 'found'
    lost = 'lost'
    choices = [(lost, 'lost'), (found, 'found')]
    status = models.CharField(max_length=10, choices=choices)
    phone = models.CharField(max_length=20, blank=True)
    # user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')


