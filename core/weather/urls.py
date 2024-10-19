from django.urls import include, path


urlpatterns = [path("api/<str:location>/", include("weather.api.urls"))]
