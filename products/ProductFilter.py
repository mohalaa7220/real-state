from django_filters import rest_framework as filters
from .models import Product


class ProductFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    min_price = filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = filters.NumberFilter(field_name='price', lookup_expr='lte')
    state = filters.CharFilter(field_name='state', lookup_expr='icontains')
    amenities = filters.CharFilter(method='filter_amenities')
    features = filters.CharFilter(method='filter_features')

    class Meta:
        model = Product
        fields = ['name', 'min_price', 'max_price', 'state', 'features',]

    def filter_amenities(self, queryset, name, value):
        if value:
            amenities = value.split(',')
            for amenity in amenities:
                queryset = queryset.filter(amenities__name=amenity)
        return queryset

    def filter_features(self, queryset, name, value):
        if value:
            features = value.split(',')
            for feature in features:
                queryset = queryset.filter(features__name=feature)
            return queryset
