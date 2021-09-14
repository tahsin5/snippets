import base64
import json
import configparser

import requests
from requests.adapters import HTTPAdapter

MAX_RETRIES = 5
TIMEOUT = 10

class ProcessRequest:
    """Send requests to external API's using python's request module.
       Sends json of response if successful.
       Raises exception otherwise.
    """

    def __init__(self, url: str, req_method: str):
        self.url = url
        self.method = req_method
        self.timeout = TIMEOUT
    
    def send_request(self, params: dict=None, headers: dict=None, payload: dict=None, files: dict=None):
        # files = {'file': open('report.xls', 'rb')}

        try:
            adapter = HTTPAdapter(max_retries=MAX_RETRIES)
            session = requests.Session()
            session.mount('https://', adapter)
            session.mount('http://', adapter)
            
            response = session.request(self.method, self.url, params=params, headers=headers, 
                                                                data=payload, files=files, timeout=self.timeout)
            if response.status_code != 200:                                     
                raise Exception(f'{response.status_code} error: {response.reason}')                                     
            return json.loads(response.content.decode('utf-8'))
            
        
        except Exception as e:
            raise Exception(e)