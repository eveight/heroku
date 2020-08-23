from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from .models import City
from .forms import CityForm


def home(request):
    qs_cities = City.objects.all()
    paginator = Paginator(qs_cities, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'cities/home.html', {'obj_list': page_obj})


def detail(request, id):
    obj = City.objects.get(id=id)
    return render(request, 'cities/detail.html', {'obj': obj})


def add(request):
    form = CityForm()
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            new_city = City()
            new_city.name = form.cleaned_data['name']
            new_city.save()
            messages.success(request, 'Город успешно добавлен')
            return redirect('city:home')
    return render(request, 'cities/add.html', {'form': form})


def edit(request, id):
    obj = City.objects.get(id=id)
    form = CityForm(instance=obj)
    if request.method == 'POST':
        form = CityForm(request.POST, instance=obj)
        if form.is_valid():
            obj.name = form.cleaned_data['name']
            obj.save()
            messages.success(request, 'Город успешно обновлен')
            return redirect('city:home')
    return render(request, 'cities/edit.html', {'form': form})


def delete(request, id):
    obj = City.objects.get(id=id)
    if request.method == 'POST':
        obj.delete()
        messages.warning(request, 'Город удалён')
        return redirect('city:home')
    return render(request, 'cities/delete.html', {'obj': obj})

