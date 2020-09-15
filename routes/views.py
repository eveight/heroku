from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RouteForm, RouteModelForm
from trains.models import Train
from .models import Route


def home(request):
    form = RouteForm()
    return render(request, 'routes/home.html', {'form': form})


def dfs_paths(graph, start, goal):
    """Функция поиска всех возможных маршрутов
       из одного города в другой. Вариант посещения
       одного и того же города более одного раза,
        не рассматривается.
    """
    stack = [(start, [start])]
    while stack:
        (vertex, path) = stack.pop()
        if vertex in graph.keys():
            for next_ in graph[vertex] - set(path):
                if next_ == goal:
                    yield path + [next_]
                else:
                    stack.append((next_, path + [next_]))


def get_graph():
    qs = Train.objects.values('from_city')
    from_city = set(i['from_city'] for i in qs)
    graph = {}
    for city in from_city:
        to_city = Train.objects.filter(from_city=city).values('to_city')
        tmp = set(i['to_city'] for i in to_city)
        graph[city] = tmp
    return graph


def find_routes(request):
    form = RouteForm()
    if request.method == 'POST':
        form = RouteForm(request.POST)
        if form.is_valid():
            from_city = form.cleaned_data['from_city']
            to_city = form.cleaned_data['to_city']
            across_cities = form.cleaned_data['across_cities']
            travel_time = form.cleaned_data['travel_time']

            graph = get_graph()
            all_ways = list(dfs_paths(graph, from_city.id, to_city.id))
            if not all_ways:
                messages.warning(request, 'Таких путей нет')
            if across_cities:
                across_city_id = [city.id for city in across_cities]
                right_ways = []
                for way in all_ways:
                    for point in across_city_id:
                        if point in way:
                            right_ways.append(way)
                if not right_ways:
                    messages.warning(request, 'Маршрут через эти города недоступен')
                    return render(request, 'routes/home.html', {'form': form})
            else:
                right_ways = all_ways

            trains = []
            total_time = 0
            for route in right_ways:
                tmp = {}
                tmp['trains'] = []
                for index in range(len(route) - 1):
                    qs = Train.objects.filter(from_city=route[index], to_city=route[index + 1])
                    qs = qs.order_by('travel_time').first()
                    total_time += qs.travel_time
                    tmp['trains'].append(qs)
                    tmp['total_time'] = total_time
                if total_time <= travel_time:
                    trains.append(tmp)
            if not trains:
                messages.warning(request, 'Время в пути больше заданого')
                return render(request, 'routes/home.html', {'form': form})

            routes = []
            cities ={'from_city': from_city.name, 'to_city': to_city.name}
            for tr in trains:
                routes.append({
                    'route': tr['trains'],
                    'total_time': tr['total_time'],
                    'from_city': from_city.name,
                    'to_city': to_city.name,
                })
            sorted_routes = []
            if len(routes) == 1:
                sorted_routes = routes
            else:
                times = list(set(x['total_time'] for x in routes))
                times = sorted(times)
                for time in times:
                    for route in routes:
                        if time == route['total_time']:
                            sorted_routes.append(route)
    return render(request, 'routes/home.html', {'form': form, 'right_ways': sorted_routes, 'cities': cities})


@login_required
def add_route(request):
    if request.method == "POST":
        form = RouteModelForm(request.POST)
        if form.is_valid():
            data = request.POST
            name = data['name']
            from_city = data['from_city']
            to_city = data['to_city']
            travel_time = data['travel_time']
            across_cities = data['across_cities'].split()
            trains = [int(x) for x in across_cities if x.isalnum()]
            qs = Train.objects.filter(id__in=trains)
            new_route = Route(name=name, from_city=from_city, to_city=to_city, travel_time=travel_time)
            new_route.save()
            for tr in qs:
                new_route.across_cities.add(tr.id)
            messages.success(request, 'Маршрут успешно создан')
            return redirect('/')

    if request.method == "GET":
        data = request.GET
        if data:
            from_city = data['from_city']
            to_city = data['to_city']
            travel_time = data['travel_time']
            across_cities = data['across_cities'].split()
            trains = [int(x) for x in across_cities if x.isalnum()]
            train_list = ' '.join(str(i) for i in trains)
            form = RouteModelForm(initial={
                'from_city': from_city,
                'to_city': to_city,
                'travel_time': travel_time,
                'across_cities': train_list,
            })
            ctx ={
                'form': form,
                'from_city': from_city,
                'to_city': to_city,
                'travel_time': travel_time,
            }
            return render(request, 'routes/add.html', ctx)
        else:
            messages.warning(request, 'Нет данных для сохрания маршрута')
            return redirect('/')


def list_routes(request):
    qs_all = Route.objects.all()
    return render(request, 'routes/list.html', {'routes': qs_all})


def detail_route(request, id):
    qs = Route.objects.get(id=id)
    return render(request, 'routes/detail_route.html', {'route': qs})


@login_required
def delete_route(request, id):
    qs = Route.objects.get(id=id)
    if request.method == 'POST':
        qs.delete()
        messages.success(request, 'Маршрут успешно удалён.')
        return redirect('list_routes')
    return render(request, 'routes/delete_route.html', {'route': qs})

