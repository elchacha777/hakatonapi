from django.db import models
from django.contrib.auth import get_user_model
"""
1) model for lost items/docs
2) model for found items/docs
"""
User = get_user_model()

class Category(models.Model):
    category = models.SlugField(primary_key=True, required=True)


class LostItem(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    name = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post')
    description = models.TextField(max_length=250)
    date_lost = models.DateField()
    image = models.ImageField()
    status = models.BooleanField()
    phone = models.CharField(max_length=20, blank=True, required=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')


class FoundItem(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE, related_name='category')
    name = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post')
    description = models.TextField(max_length=250)
    date_found = models.DateField()
    image = models.ImageField()
    status = models.BooleanField()
    phone = models.CharField(max_length=20, blank=True, required=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')

