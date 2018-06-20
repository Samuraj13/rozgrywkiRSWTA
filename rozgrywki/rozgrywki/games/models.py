from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

import datetime

from django.forms import ModelForm


class Team(models.Model):
    team_name = models.CharField(max_length=20)
    short_name = models.CharField(max_length=5)
    team_owner = models.ForeignKey('auth.User',on_delete=models.CASCADE)

    def __str__(self, **kwargs):
        return self.team_name


class Player(models.Model):
    player_name = models.CharField(max_length=20)
    player_surname = models.CharField(max_length=30)
    team_name = models.ForeignKey(Team,on_delete=models.CASCADE)

    def __str__(self, **kwargs):
        return "{Name} {Surname}".format(Name=self.player_name, Surname=self.player_surname)


class TeamScore(models.Model):
    team = models.ForeignKey(Team,on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    promote = models.BooleanField(default=False)

    def __str__(self):
        return self.team.team_name


class Event(models.Model):
    name = models.CharField(max_length=50)
    teams = models.ManyToManyField(Team, related_name='event_team')
    create_user = models.ForeignKey('auth.User', blank=True, null=True,on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class TeamEvent(models.Model):
    event = models.ForeignKey(Event,on_delete=models.CASCADE)
    team_one = models.ForeignKey(TeamScore, related_name='team_one',on_delete=models.CASCADE)
    team_two = models.ForeignKey(TeamScore, related_name='team_two',on_delete=models.CASCADE)
    is_complete = models.BooleanField(default=False)

    def __str__(self):
        return ' '.join([self.event.name, self.team_one.team.team_name, self.team_two.team.team_name])


class Match(models.Model):
    Date = models.DateField("Date", default=datetime.datetime.today)
    Host = models.ForeignKey(Team, related_name="A",on_delete=models.CASCADE)
    Guest = models.ForeignKey(Team, related_name="B",on_delete=models.CASCADE)
    Round = models.DecimalField(max_digits=2, decimal_places=0)

    def __str__(self):
        return "{Host} vs {Guest}".format(Host=self.Host.Name, Guest=self.Guest.Name)


class GlobalStat(models.Model):
    Match = models.ForeignKey(Match,on_delete=models.CASCADE)
    HostScore = models.DecimalField(max_digits=2, decimal_places=0)
    GuestScore = models.DecimalField(max_digits=2, decimal_places=0)
    HostPoints = models.DecimalField(max_digits=2, decimal_places=0)
    GuestPoints = models.DecimalField(max_digits=2, decimal_places=0)

    def __str__(self):
        return "{Host} vs {Guest}".format(Host=self.Match.Host.Name, Guest=self.Match.Guest.Name)

class Goal(models.Model):
    match = models.ForeignKey(TeamEvent,on_delete=models.CASCADE)
    player = models.ForeignKey(Player,on_delete=models.CASCADE)
    time = models.IntegerField(default=0)

    def __str__(self):
        return "{Match} {Player} {Time} {Team}".format(Match=self.match, Player=self.player, Time=self.time)


class Shot(models.Model):
    match = models.ForeignKey(TeamEvent,on_delete=models.CASCADE)
    player = models.ForeignKey(Player,on_delete=models.CASCADE)
    time = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class YellowCard(models.Model):
    match = models.ForeignKey(TeamEvent,on_delete=models.CASCADE)
    player = models.ForeignKey(Player,on_delete=models.CASCADE)
    time = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class RedCard(models.Model):
    match = models.ForeignKey(TeamEvent,on_delete=models.CASCADE)
    player = models.ForeignKey(Player,on_delete=models.CASCADE)
    time = models.IntegerField(default=0)

    def __str__(self):
        return self.name
