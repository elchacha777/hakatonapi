from django.db import models
from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from rest_framework.response import Response
from main.serializers import LostItemSerializer
from rest_framework import status
from django.db.models import Q
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
    status = models.BooleanField()
    phone = models.CharField(max_length=20, blank=True)
    # user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')

    @action(detail=False, methods=['get'])
    def search(self, request, pk=None):
        q = request.query_params.get('q')
        queryset = self.get_queryset()
        queryset = queryset.filter(Q(name__icontains=q))
        serializer = LostItemSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


