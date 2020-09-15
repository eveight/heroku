from django import forms
from cities.models import City
from .models import Route


class RouteForm(forms.Form):
    from_city = forms.ModelChoiceField(queryset=City.objects.all(), label='Откуда',
                                       widget=forms.Select(attrs={'class': 'form-control js-example-basic-single'}))
    to_city = forms.ModelChoiceField(queryset=City.objects.all(), label='Куда',
                                       widget=forms.Select(attrs={'class': 'form-control js-example-basic-single'}))
    across_cities = forms.ModelMultipleChoiceField(queryset=City.objects.all(),
                                                   label='Через какие города', required=False,
                                                   widget=forms.SelectMultiple(
                                                       attrs={'class': 'form-control js-example-basic-multiple'})
                                                   )
    travel_time = forms.IntegerField(label='Время', widget=forms.NumberInput(attrs={'class': 'form-control'}))


class RouteModelForm(forms.ModelForm):
    name = forms.CharField(label='Название маршрута', widget=forms.TextInput(attrs={'class': 'form-control'}))
    from_city = forms.CharField(widget=forms.HiddenInput())
    to_city = forms.CharField(widget=forms.HiddenInput())
    across_cities = forms.CharField(widget=forms.HiddenInput())
    travel_time = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = Route
        fields = ('name', 'from_city', 'to_city', 'across_cities', 'travel_time',)