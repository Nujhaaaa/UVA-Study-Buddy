from django import forms
from .models import TutorCourse
from bootstrap_datepicker_plus.widgets import DateTimePickerInput


class TutorCourseForm(forms.ModelForm):
    available_time_frames = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = TutorCourse
        fields = ['hourly_rate', 'available_time_frames']
        widgets = {
            'available_time_frames': DateTimePickerInput(),
        }


class SessionForm(forms.Form):
    session_time = forms.DateTimeField(
        label='Session Time',
        widget=forms.TextInput(attrs={'type': 'datetime-local'})
    )

class ThreadForm(forms.Form):
    email = forms.CharField(label='', max_length=100)

class MessageForm(forms.Form):
    message = forms.CharField(label='', max_length=1000)
