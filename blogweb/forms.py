from datetime import datetime

from django import forms
from . import models
from django.utils import timezone


class AddRollForm(forms.ModelForm):
    class Meta:
        model = models.Rolik
        fields = ['rolik_num', 'rolik_size', 'rolik_color']


class UpdateInRollForm(forms.ModelForm):
    PAY_CHOICES = (
        (10, '10 ming'),
        (15, '15 ming'),
        (20, '20 ming')
    )
    roliktime = forms.DateTimeField(initial=timezone.now(),
        input_formats=['%Y-%m-%dT%H:%M'],
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local', 'class': 'form-control'},
            format='%Y-%m-%dT%H:%M'
        ),
        label="Build Start Time",
        required=False
    )

    rolik_pay = forms.ChoiceField(choices=PAY_CHOICES, label='Select Pay', initial=10000)

    class Meta:
        model = models.InRolik
        fields = ['roliktime', 'rolik_pay']

    def clean_roliktime(self):
        roliktime = self.cleaned_data['roliktime']
        now = timezone.now()

        if roliktime and roliktime < now:
            raise forms.ValidationError("Hozirgi vaqtdan keingi keladigan vaqtni kiriting.")

        return roliktime
