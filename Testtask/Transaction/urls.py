from django.urls import path
from . import views
from django.urls import include



urlpatterns = [
    path('', views.post_new, name='post_new'),
]


urlpatterns = [
    path('', views.button_pushed, name='button_pushed'),
]