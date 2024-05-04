from django import forms
from django.forms import ModelForm
from login.models import Regulation
from django.forms import widgets
import datetime
from django.core.exceptions import ValidationError
from datetime import date


class RegulationForm(forms.ModelForm):
    class Meta:
        model = Regulation
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to form fields
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"

    # Add Bootstrap classes to form labels
    def label_tag(self, label=None, attrs=None, label_suffix=None):
        attrs = attrs or {}
        attrs["class"] = "form-label"
        return super().label_tag(label, attrs, label_suffix)

    def clean(self):
        cleaned_data = super().clean()
        winpts = cleaned_data.get("winpts")
        losepts = cleaned_data.get("losepts")
        drawpts = cleaned_data.get("drawpts")
        scoretime = cleaned_data.get("scoretime")
        minage = cleaned_data.get("minage")
        maxage = cleaned_data.get("maxage")
        minplayer = cleaned_data.get("minplayer")
        maxplayer = cleaned_data.get("maxplayer")
        maxforeignplayer = cleaned_data.get("maxforeignplayer")
        if minage < 0 or minage > maxage:
            self.add_error(
                "minage", "Min age must be greater than 0 and lower than Max age"
            )
        if maxage < minage:
            self.add_error("maxage", "Max age greater than Min age")
        if minplayer < 0 or minplayer > maxplayer:
            self.add_error(
                "minplayer",
                "Min player must be greater than 14 and lower than Max player",
            )
        if maxplayer < minplayer:
            self.add_error(
                "maxplayer",
                "Max player must be lower than 23 and greater than Min player",
            )
        if maxforeignplayer > 3 or maxforeignplayer < 0:
            self.add_error(
                "maxforeignplayer", "Max foreign player must be lower than 4"
            )
        if scoretime < 0:
            self.add_error(
                "scoretime", "Invalid max score time (Must be in range 0-90 minutes)"
            )
        if winpts < drawpts or winpts < losepts or winpts < 0:
            self.add_error(
                "winpts", "Win points must be greater than lose points and draw points"
            )
        if drawpts < losepts or drawpts > winpts or drawpts < 0:
            self.add_error(
                "drawpts",
                "Draw points must be greater than lose points and lower than win points",
            )
        if losepts > drawpts or losepts > winpts or losepts < 0:
            self.add_error(
                "losepts", "Lose points must be lower that draw points and win points"
            )
