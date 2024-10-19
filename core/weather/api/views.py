from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from django.utils import timezone
from django.core.cache import cache

from decouple import config
import requests


class WeatherViewGenericView(GenericAPIView):
    authentication_classes = []
    permission_classes = []
    base_url = "https://api.weatherapi.com/v1/current.json"
    api_key = config("WEATHER_API_KEY")

    def get(self, request, location, *args, **kwargs):
        if not cache.get(f"{timezone.now().day}-{location}"):
            url = self.get_url(location)
            response = requests.get(url)
            if response.status_code == 200:
                # cache successfull requests.(location is valid & connection is valid.)
                cache.set(
                    f"{timezone.now().day}-{location}", response.json(), timeout=20 * 60
                )
            else:
                # for 400 requests.
                return Response(response.json())

        # get data from cach and send it.
        data = cache.get(f"{timezone.now().day}-{location}")
        return Response(data)

    def get_url(self, location):
        return self.base_url + f"?q={location}&key=" + self.api_key
