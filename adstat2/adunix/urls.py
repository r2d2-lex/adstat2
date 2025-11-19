from django.urls import path
from .views import index, get_user_data, update_user_data, delete_user_data, get_new_uid, get_new_gid

app_name = 'adunix'
urlpatterns = [
    path('', index, name='index'),
    path('get_user_data/', get_user_data, name='get_user_data'),
    path('update_user_data/', update_user_data, name='update_user_data'),
    path('delete_user_data/', delete_user_data, name='delete_user_data'),
    path('get_new_uid/', get_new_uid, name='get_new_uid'),
    path('get_new_gid/', get_new_gid, name='get_new_gid'),
]
