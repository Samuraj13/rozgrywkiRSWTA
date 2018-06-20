from django.contrib import admin
from .models import Team, Player, Event, TeamEvent, TeamScore, Goal, Shot, YellowCard, RedCard


class admin_teams(admin.ModelAdmin):
    list_display = ('team_name', 'short_name','team_owner')

class admin_players(admin.ModelAdmin):
    list_display = ('player_name', 'player_surname', 'team_name')

admin.site.register(Team, admin_teams)
admin.site.register(Player, admin_players)
admin.site.register(Event)
admin.site.register(TeamEvent)
admin.site.register(TeamScore)
admin.site.register(Goal)
admin.site.register(Shot)
admin.site.register(YellowCard)
admin.site.register(RedCard)

