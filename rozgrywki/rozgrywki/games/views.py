from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.views import View
from django.urls import reverse
from django.views.generic import DetailView
from django.db.models import Count, F, Sum, Q

from rozgrywki.games.forms import EventForm
from .models import Team, TeamEvent, Event, TeamScore, Player, GlobalStat, Goal, Shot, YellowCard, RedCard


def MatchListView(request, r):
    match = GlobalStat.objects.filter(Match__Round__exact=r)
    return render(request, 'play/globalstat_list.html', {'match_list': match})

def home(request):
    players = Player.objects.annotate(gole=Count('goal')).order_by('-gole')
    events = Event.objects.all()
    gole = Team.objects.all().annotate(ilosc=Sum('teamscore__score', distinct=True)).order_by('-ilosc')
    context = {
        'events': events,
        'players': players,
        'gole': gole
    }
    return render(request, 'home.html',context)

def team_view(request):

   teams = Team.objects.filter(team_owner=request.user)
   context = {
        'teams': teams,
    }
   return render(request, 'games/team_list.html',context)

def player_detail(request, pkTeam, pkPlayer):
   team = get_object_or_404(Team, pk=pkTeam)
   player = Player.objects.filter(id=pkPlayer)
   gole = Player.objects.annotate(goals=Count('goal'))
   strzaly = Player.objects.annotate(shots=Count('shot'))
   zoltekartki = Player.objects.annotate(yellowcards=Count('yellowcard'))
   czerwonekartki = Player.objects.annotate(redcards=Count('redcard'))
   context = {
        'team': team,
        'players': player,
        'gole': gole,
        'strzaly': strzaly,
        'zoltekartki': zoltekartki,
        'czerwonekartki': czerwonekartki,
    }
   return render(request, 'games/player_detail.html',context)

class EventViewSet(View):

    def get(self, request):
        if request.user.is_authenticated or request.user.is_staff:
            events = Event.objects.filter(create_user_id=request.user.id)
            form = EventForm(request=request)
            return render(request, 'my_events.html', {'events': events, 'user': request.user, 'form': form})
        return Http404

    def post(self, request):
        form = EventForm(request.POST)
        event = form.save()
        event.create_user = request.user
        event.save()
        for team_one in event.teams.all():
            for team_two in event.teams.all():
                if team_one != team_two:
                    t1 = TeamScore.objects.create(
                        team=team_one
                    )
                    t2 = TeamScore.objects.create(
                        team=team_two
                    )
                    TeamEvent.objects.create(
                        event=event,
                        team_one=t1,
                        team_two=t2
                    )

        return redirect('bracket', pk=event.id)

class CreateEventViewSet(View):

    def get(self, request):
        if request.user.is_authenticated or request.user.is_staff:
            form = EventForm(request=request)
            return render(request, 'create_event.html', {'form': form})
        return Http404

    def post(self, request):
        form = EventForm(request.POST)
        event = form.save()
        event.create_user = request.user
        event.save()
        for team_one, team_two in zip(event.teams.all()[0::2], event.teams.all()[1::2]):
            t1 = TeamScore.objects.create(
                team=team_one
            )
            t2 = TeamScore.objects.create(
                team=team_two
            )
            TeamEvent.objects.create(
                event=event,
                team_one=t1,
                team_two=t2
            )

        return redirect('bracket', pk=event.id)


class BracketViewSet(View):
    def get(self, request, pk):
        try:
            event = Event.objects.get(id=pk)
            teams = TeamEvent.objects.filter(event_id=event.id)
            players = Player.objects.annotate(gole=Count('goal')).order_by('-gole')
            events = Player.objects.all()
            gole = Team.objects.all().annotate(ilosc=Sum('teamscore__score', distinct=True)).annotate(mecze=Count('teamscore__team_id')).annotate(punkty=Sum('event_team')).order_by('-ilosc')

            return render(request, 'event_bracket.html',
                          context={
                              'event': event,
                              'teams': teams,
                              'events': events,
                              'players': players,
                              'gole': gole,
                          })
        except Event.DoesNotExist:
            return Http404


class TeamDetailsView(DetailView):
    model = Team

def EditBracket(request, pk):
    try:
        event = Event.objects.get(id=pk)
        teamscores = TeamEvent.objects.filter(event_id=event.id)
        return render(request, 'event_edit.html',
                      context={
                          'event': event,
                          'teamscores': teamscores
                      })
    except Event.DoesNotExist:
        return Http404

def ShowMatch(request, pk):
    try:
        teamscores = TeamEvent.objects.filter(id=pk)
        gole = Goal.objects.filter(match=pk).order_by('time')
        strzaly = Shot.objects.filter(match=pk).order_by('time')
        zoltekartki = YellowCard.objects.filter(match=pk).order_by('time')
        czerwonekartki = RedCard.objects.filter(match=pk).order_by('time')

        return render(request, 'match_details.html',
                      context={
                          'teamscores': teamscores,
                          'gole': gole,
                          'strzaly': strzaly,
                          'zoltekartki': zoltekartki,
                          'czerwonekartki': czerwonekartki
                      })
    except Event.DoesNotExist:
        return Http404


def EditMatch(request, pk):
    try:
        teamscores = TeamEvent.objects.filter(id=pk)
        players = Player.objects.all()
        gole = Player.objects.filter(goal__match=pk).annotate(goals=Count('goal', distinct=True))
        strzaly = Player.objects.filter(goal__match=pk).annotate(shots=Count('shot', distinct=True))
        zoltekartki = Player.objects.filter(goal__match=pk).annotate(yellowcards=Count('yellowcard', distinct=True))
        czerwonekartki = Player.objects.filter(goal__match=pk).annotate(redcards=Count('redcard', distinct=True))

        return render(request, 'match_edit.html',
                      context={
                          'teamscores': teamscores,
                          'gole': gole,
                          'strzaly': strzaly,
                          'zoltekartki': zoltekartki,
                          'czerwonekartki': czerwonekartki,
                          'players': players
                      })
    except Event.DoesNotExist:
        return Http404

def AddPlayer(request, pk):
    if request.user.is_authenticated or request.user.is_staff:
        try:
            team = get_object_or_404(Team, pk=pk)
            player = Player.objects.get_or_create(player_name=request.POST['player_name'], player_surname=request.POST['player_surname'], team_name=team)
            return redirect('team-details', pk)
        except (KeyError):
            return render_to_response('/', {
                'error_message': "Bad choice",
            })
    return Http404

def RemovePlayer(request, pk):
    if request.user.is_authenticated or request.user.is_staff:
        try:
            team = get_object_or_404(Team, pk=pk)
            player = get_object_or_404(Player, player_name=request.POST['player_name'], player_surname=request.POST['player_surname'], team_name=team)
            player.delete()
            return redirect('team-details', pk)
        except (KeyError):
            return render_to_response('/', {
                'error_message': "Bad choice",
            })
    return Http404

def AddTeam(request):
    try:
        team = Team.objects.get_or_create(team_name=request.POST['team_name'],team_owner=request.user,short_name=request.POST['short_name'])
        return redirect('team-list', )
    except (KeyError):
        return render_to_response('/', {
            'error_message': "Bad choice",
        })

def AddGoal(request, pk):
    if request.user.is_authenticated or request.user.is_staff:
        try:
            data = request.POST['player']
            splitted = data.split()
            player_id = Player.objects.get(player_name = splitted[0])
            match_id = TeamEvent.objects.get(id=int(request.POST['match_id']))
            goal = Goal.objects.get_or_create(match=match_id, player = player_id, time=int(request.POST['time']))
            if match_id.team_one.team == player_id.team_name:
                TeamScore.objects.filter(id=match_id.team_one.id).update(score=F('score')+1)
            else:
                TeamScore.objects.filter(id=match_id.team_two.id).update(score=F('score') + 1)

            return redirect('match-edit', pk)
        except Event.DoesNotExist:
            return Http404

def AddShot(request, pk):
    if request.user.is_authenticated or request.user.is_staff:
        try:
            data = request.POST['player']
            splitted = data.split()
            player_id = Player.objects.get(player_name = splitted[0], player_surname= splitted[1])
            match_id = TeamEvent.objects.get(id=int(request.POST['match_id']))
            shot = Shot.objects.get_or_create(match=match_id, player = player_id, time=int(request.POST['time']))
            return redirect('match-edit', pk)
        except Event.DoesNotExist:
            return Http404

def AddYellowCard(request, pk):
    if request.user.is_authenticated or request.user.is_staff:
        try:
            data = request.POST['player']
            splitted = data.split()
            player_id = Player.objects.get(player_name = splitted[0], player_surname= splitted[1])
            match_id = TeamEvent.objects.get(id=int(request.POST['match_id']))
            yellowcard = YellowCard.objects.get_or_create(match=match_id, player = player_id, time=int(request.POST['time']))
            return redirect('match-edit', pk)
        except Event.DoesNotExist:
            return Http404

def AddRedCard(request, pk):
    if request.user.is_authenticated or request.user.is_staff:
        try:
            data = request.POST['player']
            splitted = data.split()
            player_id = Player.objects.get(player_name = splitted[0], player_surname= splitted[1])
            match_id = TeamEvent.objects.get(id=int(request.POST['match_id']))
            redcard = RedCard.objects.get_or_create(match=match_id, player = player_id, time=int(request.POST['time']))
            return redirect('match-edit', pk)
        except Event.DoesNotExist:
            return Http404

def MatchEnd(request, pk):
    if request.user.is_authenticated or request.user.is_staff:
        try:
            TeamEvent.objects.filter(id=pk).update(is_complete=True)
            return redirect('match-edit', pk)
        except Event.DoesNotExist:
            return Http404

def MatchResume(request, pk):
    if request.user.is_authenticated or request.user.is_staff:
        try:
            TeamEvent.objects.filter(id=pk).update(is_complete=False)
            return redirect('match-edit', pk)
        except Event.DoesNotExist:
            return Http404

def RemoveTeam(request):
    if request.user.is_authenticated or request.user.is_staff:
        try:
            #team = get_object_or_404(Team, team_name=request.POST['team_name'])
            Team.objects.filter(short_name=request.POST["a"]).delete()
            return redirect('team-list', )
        except (KeyError):
            return render_to_response('/', {
                'error_message': "Bad choice",
            })
    return Http404


def RemoveEvent(request):
    if request.user.is_authenticated or request.user.is_staff:
        try:
            #event = get_object_or_404(Event, name=request.POST['event_name'])
            Event.objects.filter(name=request.POST['event_name']).delete()
            return redirect('events',)
        except (KeyError):
            return render_to_response('/', {
                'error_message': "Bad choice",
            })
    return Http404


