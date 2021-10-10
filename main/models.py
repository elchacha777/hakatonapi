from django.db import models
from django.contrib.auth import get_user_model

from account.models import MyUser

"""
1) model for lost items/docs
2) model for found items/docs
"""


class Category(models.Model):
    slug = models.SlugField(max_length=50, primary_key=True)
    name = models.CharField(unique=True, max_length=255)

    def __str__(self):
        return self.name


class Item(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='item')
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='item')
    title = models.CharField(max_length=100, )
    description = models.TextField(max_length=250)
    date_lost = models.DateField()
    found = 'found'
    lost = 'lost'
    choices = [(lost, 'lost'), (found, 'found')]
    status = models.CharField(max_length=10, choices=choices)

    def __str__(self):
        return self.title


class Image(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='images')

