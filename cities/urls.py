from django.urls import path
from .views import home, detail, add, edit, delete

urlpatterns = [
    path('', home, name='home'),
    path('detail/<int:id>/', detail, name='detail'),
    path('edit/<int:id>/', edit, name='edit'),
    path('delete/<int:id>/', delete, name='delete'),
    path('add/', add, name='add'),
]
