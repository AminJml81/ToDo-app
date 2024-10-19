from django.urls import path
from django.views.decorators.cache import cache_page

from .views import WeatherViewGenericView


urlpatterns = [path("", WeatherViewGenericView.as_view(), name="current-weather")]
