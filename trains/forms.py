from django import forms
from .models import Train
from cities.models import City


class TrainForm(forms.ModelForm):
    name = forms.CharField(label='Поезд', widget=forms.TextInput(attrs={
                            'class': "form-control",
                            'placeholder': 'Введите номер поезда:'
                            }))
    from_city = forms.ModelChoiceField(queryset=City.objects.all(), label='Откуда', widget=forms.Select(attrs={
                                            'class': "form-control",
                                            }))
    to_city = forms.ModelChoiceField(queryset=City.objects.all(), label='Куда', widget=forms.Select(attrs={
                                            'class': "form-control",
                                            }))
    travel_time = forms.IntegerField(label='Часов в пути', widget=forms.NumberInput(attrs={
                                    'class': "form-control",
                                    }))

    class Meta:
        model = Train
        fields = ('name', 'from_city', 'to_city', 'travel_time')