from django.db import models
from django.contrib.auth import get_user_model

"""
1) model for lost items/docs
2) model for found items/docs
"""
User = get_user_model()


class Category(models.Model):
    category = models.SlugField(primary_key=True)

    def __str__(self):
        return self.category


class LostItem(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='item')
    title = models.CharField(max_length=100, )
    description = models.TextField(max_length=250)
    date_lost = models.DateField()
    found = 'found'
    lost = 'lost'
    # image = models.ImageField(upload_to='items/', blank=True, null=True)
    choices = [(lost, 'lost'), (found, 'found')]
    status = models.CharField(max_length=10, choices=choices)
    phone = models.CharField(max_length=20, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')

    def __str__(self):
        return self.title


class ItemImage(models.Model):
    Item = models.ForeignKey(LostItem, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='items/', blank=True, null=True)

    def __str__(self):
        if self.image:
            return self.image.url
        return ''