from django import forms
from parts.models import Part

class AircraftAssembleForm(forms.Form):
    parts = forms.ModelMultipleChoiceField(queryset=Part.objects.none(), widget=forms.CheckboxSelectMultiple)

    def __init__(self, *args, team=None, **kwargs):
        super().__init__(*args, **kwargs)
        if team:
            self.fields['parts'].queryset = Part.objects.filter(team=team, used=False)