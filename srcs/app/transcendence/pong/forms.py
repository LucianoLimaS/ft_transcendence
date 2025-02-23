from django import forms
from django.utils.translation import gettext as getTranslated
from .models import PongRoom, Tournament


class PongRoomForm(forms.ModelForm):
    class Meta:
        model = PongRoom
        fields = ["name"]
        labels = {
            "name": "",
        }
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control rounded-5 border-0",
                    "placeholder": "Choose a name",
                    "title": "room-name.",
                    "maxlength": "50",
                }
            ),
        }


class TournamentForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = ["name"]
        labels = {
            "name": "",
        }
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control rounded-5 border-0",
                    "placeholder": "Choose a name",
                    "title": "tournament-name",
                    "maxlength": "50",
                }
            ),
        }
