import requests

from odoo import http
from odoo.http import route
from odoo.http import request


class Main(http.Controller):
    @route("/current_weather", auth="user", type="json")
    def current_weather(self):
        """
        Fetch the current weather data from OpenWeather
        """

        API_KEY = "689a3aae2a66650806635d44529f5590"
        city_name = request.env.user.city
        country_code = request.env.user.country_code
        unit = "metric"

        api_url = "https://api.openweathermap.org/data/2.5/weather"
        query_params = f"?q={city_name},{country_code}&appid={API_KEY}&units={unit}"

        url = api_url + query_params
        response = requests.get(url, timeout=5)
        return response.json()
