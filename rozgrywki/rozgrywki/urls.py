from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.contrib import admin

from rozgrywki.core.filters import UserFilter, TeamFilter, EventFilter
from django_filters.views import FilterView
from rozgrywki.core import views as core_views
from rozgrywki.games import views as games_views
from rozgrywki.core.views import search
from rozgrywki.games.views import BracketViewSet, CreateEventViewSet, EventViewSet, TeamDetailsView, AddPlayer, RemovePlayer, AddTeam, RemoveTeam, RemoveEvent, AddGoal, AddShot, AddYellowCard, AddRedCard, MatchResume, MatchEnd

urlpatterns = [
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^$', games_views.home, name='home'),
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'home'}, name='logout'),
    url(r'^signup/$', core_views.signup, name='signup'),
    url(r'^events/$', EventViewSet.as_view(), name='events'),
    url(r'^create_event/$', CreateEventViewSet.as_view(), name='create_event'),
    url(r'^remove_event/$', RemoveEvent, name='remove-event'),
    url(r'^add_goal/(?P<pk>[0-9]+)/$', AddGoal, name='add-goal'),
    url(r'^add_shot/(?P<pk>[0-9]+)/$', AddShot, name='add-shot'),
    url(r'^add_yellowcard/(?P<pk>[0-9]+)/$', AddYellowCard, name='add-yellowcard'),
    url(r'^add_redcard/(?P<pk>[0-9]+)/$', AddRedCard, name='add-redcard'),
    url(r'^bracket/(?P<pk>[0-9]+)/$', BracketViewSet.as_view(), name='bracket'),
    url(r'^bracket/(?P<pk>[0-9]+)/edit$', games_views.EditBracket, name='bracket-edit'),
    url(r'^match/(?P<pk>[0-9]+)/$', games_views.ShowMatch, name='match-details'),
    url(r'^match/(?P<pk>[0-9]+)/edit$', games_views.EditMatch, name='match-edit'),
    url(r'^match/(?P<pk>[0-9]+)/end$', MatchEnd, name='match-end'),
    url(r'^match/(?P<pk>[0-9]+)/resume$', MatchResume, name='match-resume'),
    url(r'^account_activation_sent/$', core_views.account_activation_sent, name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        core_views.activate, name='activate'),
    url(r'^games/', games_views.home, name = 'games'),
    url(r'^teams/(?P<pk>\d+)$', TeamDetailsView.as_view(), name='team-details'),
    url(r'^teams/(?P<pk>\d+)/footballers/add/$', AddPlayer, name='add-player'),
    url(r'^teams/(?P<pk>\d+)/footballers/remove/$', RemovePlayer, name='remove-player'),
    url(r'^teams/add/$', AddTeam, name='add-team'),
    url(r'^teams/remove/$', RemoveTeam, name='remove-team'),
    url(r'^teams/(?P<pkTeam>\d+)/(?P<pkPlayer>\d+)$', games_views.player_detail, name='player-details'),
    url(r'^teams/$', games_views.team_view, name='team-list'),
    url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
    url(r'^search/', search, name = 'search'),
    url(r'^team_search/$', FilterView.as_view(filterset_class=TeamFilter,
        template_name='team_list.html'), name='team_search'),
    url(r'^user_search/$', FilterView.as_view(filterset_class=UserFilter,
        template_name='user_list.html'), name='user_search'),
    url(r'^event_search/$', FilterView.as_view(filterset_class=EventFilter,
        template_name='event_list.html'), name='event_search'),

]
