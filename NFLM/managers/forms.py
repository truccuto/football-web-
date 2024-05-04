from django import forms
from django.forms import ModelForm
from login.models import Coach, Regulation
from django.forms import widgets
import datetime
from django.core.exceptions import ValidationError
from datetime import date
# Create a Player form

class CoachSearchForm(forms.Form):
    coach_name = forms.CharField(label='Coach Name', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Search', 'name': 'coach_name'}))

class CoachForm(ModelForm):
    class Meta:
        model = Coach
        fields = "__all__"
    
    coach_image = forms.ImageField(required=True)
    dob = forms.DateField(widget=widgets.DateInput(attrs={'type': 'date'}), initial=datetime.date.today())
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to form fields
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    # Add Bootstrap classes to form labels
    def label_tag(self, label=None, attrs=None, label_suffix=None):
        attrs = attrs or {}
        attrs['class'] = 'form-label'
        return super().label_tag(label, attrs, label_suffix)
    def clean(self):
        cleaned_data = super().clean()
        dob = cleaned_data.get('dob')
        regulation = Regulation.objects.get(pk=1)
        # Kiểm tra tuổi cầu thủ hợp lệ hay không
        if dob:
            today = date.today()
            age = today.year - dob.year

            if age < regulation.minage:
                self.add_error('dob', "Invalid date of birth. Manager's age must greater than "+ str(regulation.minage)+".")
    