from django import forms

from rozgrywki.games.models import Event, Team


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ('team_name',)


class EventForm(forms.ModelForm):
    name = forms.CharField(max_length=50)
    teams = forms.ModelMultipleChoiceField(queryset=Team.objects.all())

    class Meta:
        model = Event
        fields = ('name', 'teams')



    def __init__(self, *args, **kwargs):
        self.request = None
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(EventForm, self).__init__(*args, **kwargs)
        if self.request:
            self.fields['teams'].queryset = Team.objects.filter(team_owner=self.request.user)


