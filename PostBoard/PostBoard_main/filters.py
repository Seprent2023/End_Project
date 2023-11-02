from django_filters import FilterSet, DateTimeFilter
from django.forms import DateTimeInput
from .models import Posts


class PostFilter(FilterSet):
    time_in_filter = DateTimeFilter(
        field_name='time_in',
        lookup_expr='gt',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'},
        )
    )

    class Meta:
        model = Posts
        fields = {
            'headline': ['icontains'],
            'category': ['exact'],
        }
