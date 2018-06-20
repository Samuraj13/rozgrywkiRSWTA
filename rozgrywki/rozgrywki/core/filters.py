from django.contrib.auth.models import User
from rozgrywki.games.models import Team, Event
import django_filters

class UserFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(lookup_expr='icontains')
    username = django_filters.CharFilter(lookup_expr='icontains')
    last_name = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', ]


class TeamFilter(django_filters.FilterSet):
    team_name = django_filters.CharFilter(lookup_expr='icontains')
    short_name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Team
        fields = ['team_name', 'short_name', ]


class EventFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Event
        fields = ['name', ]

