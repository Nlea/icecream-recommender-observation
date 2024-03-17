import requests
from requests.exceptions import HTTPError
import os
from dotenv import load_dotenv
from opentelemetry import trace


class Geolocator(object):
    def __init__(self, location):
        self.location = location
        load_dotenv()
        api_key=os.environ.get("POSITIONSTACK_API_KEY")
        self.url = "http://api.positionstack.com/v1/forward?access_key=" + api_key + "&query=" + location
    

    def getLocationDetails(self, ctx, headers):
        tracer = trace.get_tracer(__name__)

        payload = {}
        print(f'this is the context for the get call ${ctx}')
        #headers = headers
        with tracer.start_span("get geo data", context=ctx):
            try:
                response = requests.request("GET", self.url, headers=headers, data=payload)
                jsonResponse = response.json()
                latitude =jsonResponse["data"][0]["latitude"]
                longitude = jsonResponse["data"][0]["longitude"]
                location_data = {"latitude": latitude, "longitude": longitude}
                return location_data
            
            except HTTPError as http_err:
                print(f'HTTP error: {http_err}')
                return http_err
            ##except:
                ##print('Other error')
                ##return "Another error"