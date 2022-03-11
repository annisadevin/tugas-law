from django.urls import path
from . import views

app_name = 'oauth'

urlpatterns = [
    path('token', views.token, name='token'),
    path('resource', views.resource, name='resource'),
]
