

import json
import os
from dotenv import load_dotenv
import requests


class OctoPrintValues:
    """
    This Class stores the values from the OctoPrintAPI Class
    """

    def __init__(self):
        self.isPrinting = False
        self.progress = 0

    # --- is printing --- #
    def set_isPrinting(self, isPrinting):
        self.isPrinting = isPrinting
        
    def get_isPrinting(self):
        return self.isPrinting

    # --- Progress --- #
    def set_progress(self, progress):
        self.progress = progress

    def get_progress(self) -> int:
        return int(self.progress)


class OctoPrintAPI:
    """
    This Class is an interface for the Octoprint server API
    """

    def __init__(self, host="octopi.local", port=80):
        # Loads the enviroment variables (api keys)
        load_dotenv()
        
        self.host = host
        self.port = port
        self.api_key = os.getenv("API_KEY")
        self.session = requests.Session()
            
        self.session.headers.update({'X-Api-Key': self.api_key,
                               'Content-Type': 'application/json'})

        # Base address for all the requests
        self.base_address = 'http://' + self.host + ':' + str(self.port)
    
    
    def is_printer_connected(self):
        """
        Checks if the printer is connected to the Octoprint server

        Returns:
            String: Returns the 'operational' value if connected
            Boolean: Returns False if the printer is not connected
        """

        try:
            r = self.session.get(self.base_address + '/api/printer')
        except Exception as Ex:
            return False
        
        else:
            if r.status_code != 200:
                print(f"ERROR: Status code {r.status_code}")
                print(f"ERROR: {r.content.decode('utf-8')}")
                return False
                
            try:
                return json.loads(r.content.decode('utf-8'))["state"]["flags"]["operational"]
            except Exception as Ex:
                print(f"Unable to load result!\n{Ex}")
                return False


    def get_printer_status(self):
        """
        Get the printer status

        Returns:
            String: Returns the json string value if recieves a 200 status
            Boolean: Returns False if unable to get status
        """
        
        try:
            r = self.session.get(self.base_address + '/api/printer')
        except Exception as Ex:
            print(f"Unable to get base address!")
            return False
        
        else:
            if r.status_code != 200:
                print(f"ERROR: Status code {r.status_code}")
                print(f"ERROR: {r.content.decode('utf-8')}")
                return False
            
            try:
                return json.loads(r.content.decode('utf-8'))["state"]["text"]
            except Exception as Ex:
                print("ERROR: Unable to parse json")
                print(f"{Ex.__cause__} \n {Ex.__traceback__}")
                return False


    def get_print_progress(self):
        """
        Get the print progress as a percentage

        Returns:
            int: The progress of the printer
            Boolean: Returns False if unable to get progress
        """
        
        try:
            results = self.session.get(self.base_address + '/api/job')
        except Exception as Ex:
            print(f"{Ex.__cause__} \n {Ex.__traceback__}")
            return False
        
        else:
            if results.status_code != 200:
                print(f"ERROR: Status code {results.status_code}")
                print(f"ERROR: {results.content.decode('utf-8')}")
                return False
            
            try:
                return json.loads(results.content.decode('utf-8'))["progress"]["completion"]
            except Exception as Ex:
                print("ERROR: Unable to parse json")
                print(f"{Ex.__cause__} \n {Ex.__traceback__}")
                return False
