"""ways URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from routes.views import home, find_routes, add_route, list_routes, detail_route, delete_route

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cities/', include(('cities.urls', 'city'))),
    path('trains/', include(('trains.urls', 'train'))),
    path('user/', include(('user.urls', 'user'))),
    path('', home, name='home'),
    path('find-routes', find_routes, name='find_routes'),
    path('add-route', add_route, name='add_route'),
    path('list', list_routes, name='list_routes'),
    path('detail-route/<int:id>', detail_route, name='detail_route'),
    path('delete-route/<int:id>', delete_route, name='delete_route'),
]
