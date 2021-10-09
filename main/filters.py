import django_filters
from django_filters.rest_framework import FilterSet
from main.models import LostItem


class ItemsFilter(FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    description = django_filters.CharFilter(field_name='description', lookup_expr='icontains')
    date_from = django_filters.DateTimeFilter(field_name='date_lost', lookup_expr='gte')
    date_to = django_filters.DateTimeFilter(field_name='date_lost', lookup_expr='lte')

    class Meta:
        model = LostItem
        fields = ('category', 'title', 'description', 'date_from', 'date_to')
