import requests

from Serialization.response import ApiResponse


class RailAPIClient:
    def __init__(self, base_url="https://israelrail.azurefd.net/rjpa-prod/api/v1/timetable/"):
        self.base_url = base_url

    def get_schedule(self, from_station, to_station, date, hour, schedule_type=1, system_type=2, language_id="Hebrew"):
        params = {
            "fromStation": from_station,
            "toStation": to_station,
            "date": date,
            "hour": hour,
            "scheduleType": schedule_type,
            "systemType": system_type,
            "languageId": language_id
        }
        endpoint = "searchTrainLuzForDateTime"
        full_url = self.base_url + endpoint
        payload = {}
        headers = {
            'authority': 'israelrail.azurefd.net',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9,ru;q=0.8,he;q=0.7,de;q=0.6',
            'access-control-allow-origin': '*',
            'ocp-apim-subscription-key': '4b0d355121fe4e0bb3d86e902efe9f20',
            'origin': 'https://www.rail.co.il',
            'referer': 'https://www.rail.co.il/',
            'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
        }

        print("Отправляемый URL:", full_url, "с параметрами:", params)
        response = requests.get(full_url, params=params, headers=headers)
        response.raise_for_status()
        api_response = ApiResponse.parse_obj(response.json())

        return api_response


