from django.urls import path
from .views import index, get_user_data, update_user_data, delete_user_data

app_name = 'adunix'
urlpatterns = [
    path('', index, name='index'),
    path('get_user_data/', get_user_data, name='get_user_data'),
    path('update_user_data/', update_user_data, name='update_user_data'),
    path('delete_user_data/', delete_user_data, name='delete_user_data'),
]
