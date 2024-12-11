from django.urls import path
from .views import index

app_name = 'adunix'
urlpatterns = [
    path('', index, name='index'),
]
