from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from main.models import *
from main.permissions import IsAuthorPermission
from main.serializers import *
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q


class PermissionMixin:
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permissions = [IsAuthorPermission, ]
        else:
            permissions = []
        return [permission() for permission in permissions]


class CategoryViewSet(PermissionMixin, ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        category_filter = self.request.query_params.get('category', '')
        if category_filter == self.request.query_params.get('category'):
            queryset = queryset.filter(category=category_filter)
        return queryset


class LostItemViewSet(PermissionMixin, ModelViewSet):
    queryset = LostItem.objects.all()
    serializer_class = LostItemSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['action'] = self.action
        return context


    # @action(detail=False, methods=['get'])
    # def search(self, request, pk=None):
    #     q = request.query_params.get('q')
    #     queryset = self.get_queryset()
    #     queryset = queryset.filter(Q(name__icontains=q))
    #     serializer = LostItemSerializer(queryset, many=True, context={'request': request})
    #     return Response(serializer.data, status=status.HTTP_200_OK)
