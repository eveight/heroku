from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib import messages

from trains.forms import TrainForm
from trains.models import Train


def home(request):
    qs_trains = Train.objects.all()
    paginator = Paginator(qs_trains, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'trains/home.html', {'obj_list': page_obj})


def add(request):
    form = TrainForm()
    if request.method == 'POST':
        form = TrainForm(request.POST)
        if form.is_valid():
            new_train = Train()
            new_train.name = form.cleaned_data['name']
            new_train.from_city = form.cleaned_data['from_city']
            new_train.to_city = form.cleaned_data['to_city']
            new_train.travel_time = form.cleaned_data['travel_time']
            new_train.save()
            messages.success(request, 'Поезд успешно добавлен')
            return redirect('train:home')
    return render(request, 'trains/add.html', {'form': form})


def detail(request, id):
    obj = Train.objects.get(id=id)
    return render(request, 'trains/detail.html', {'obj': obj})


def edit(request, id):
    obj = Train.objects.get(id=id)
    form = TrainForm(instance=obj)
    if request.method == 'POST':
        form = TrainForm(request.POST, instance=obj)
        if form.is_valid():
            obj.name = form.cleaned_data['name']
            obj.from_city = form.cleaned_data['from_city']
            obj.to_city = form.cleaned_data['to_city']
            obj.travel_time = form.cleaned_data['travel_time']
            obj.save()
            messages.success(request, 'Поезд успешно обновлен')
            return redirect('train:home')
    return render(request, 'trains/edit.html', {'form': form})


def delete(request, id):
    obj = Train.objects.get(id=id)
    if request.method == 'POST':
        obj.delete()
        messages.warning(request, 'Поезд удалён')
        return redirect('train:home')
    return render(request, 'trains/delete.html', {'obj': obj})