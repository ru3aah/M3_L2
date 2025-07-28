from django_filters import DateFilter
from django_filters.rest_framework import FilterSet
from ..models import Post

class PostFilter(FilterSet):
   created_before = DateFilter(field_name='created_at', lookup_expr='lte')
   created_after = DateFilter(field_name='created_at', lookup_expr='gte')

   class Meta:
      model = Post
      fields = ['category', 'tags', 'created_before', 'created_after']

