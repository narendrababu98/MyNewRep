import requests
import json


class ApiData:
    def __init__(self):
        self.url = "https://latest-mutual-fund-nav.p.rapidapi.com/latest"

    def get_fund_data(self):
        querystring = {"Scheme_Type": "Open"}

        headers = {
            "x-rapidapi-key": "4eac90bb8dmshf006b260c6bc870p1c7dffjsnc0fff7738754",
            "x-rapidapi-host": "latest-mutual-fund-nav.p.rapidapi.com"
        }
        response = requests.get(self.url, headers=headers, params=querystring)
        return response




