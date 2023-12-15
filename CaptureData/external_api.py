import requests

LOCATION_ENDPOINT = "https://restcountries.com/v3.1/all"

class LocationSearch:

    def __init__(self) -> None:
        self.country_name = []

    def get_location_list(self):
        response = requests.get(url=LOCATION_ENDPOINT)
        data = response.json()
        for name in data:
            self.country_name.append(name["name"]["common"])

        return self.country_name