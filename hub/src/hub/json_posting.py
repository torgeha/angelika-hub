
import requests
import json


class JsonPosting:

    def post_file(self, file_to_post, username=None, password=None, token=None):
        """
        Tries to authenticate based on username/password if token is not provided.
        Posts provided file to API. THROES EXCEPTION! Must be handled!
        """

        # If no token is given, username and password is needed to provide new token
        if not token:
            token = self.authenticate(username, password)

        with open(file_to_post) as json_file:

            # Get the json data from file
            payload = json.load(json_file)

            url = "http://127.0.0.1:8000/post-measurements/" # Remember trailing slash

            headers = {'content-type': 'application/json', 'Authorization': "Token " + token}

            r = requests.post(url, data=json.dumps(payload), headers=headers)

            print r.status_code

            self.raise_exception_if_bad_request(r)

            #For testing
            # Create log file with response, for debugging
            # f = open("log.html", "w")
            # f.write(r.text)
            # f.close()

        return token

    def authenticate(self, username, password):
        """
        Tries to authenticate the hub based on username and password. Raises exception if response status code is not
        2xx. I.e username or password is wrong or serverside error.
        """

        url = "http://127.0.0.1:8000/api-token-auth/" # Remember trailing slash
        headers = {'content-type': 'application/json'}

        r = requests.post(url, data=json.dumps({"username": username, "password": password}), headers=headers)

        print r.status_code

        self.raise_exception_if_bad_request(r)
        parsed_response = json.loads(r.text)

        print "Token returned: ", parsed_response['token']

        return parsed_response['token']

    def raise_exception_if_bad_request(self, request):
        if not request.status_code == requests.codes.ok:
            request.raise_for_status() # If status code is not a 2xx, exception will be raised
            # TODO: Handle exception



# Testing
ps = JsonPosting()

# print ps.post_file("test_observation.json", username="trd-hub-1", password="123")

print ps.post_file("test_observation.json", token="6ac8a69bdac5eca659b983dce3b29255af9b00e6")

"""
payload = {"Observation" :{"hub_id": 1234},"Measurements":
    [
        {"date": 1413410400, "type": "steps", "unit":"steps", "value": 666},
        {"date": 1413410400, "type": "soft", "unit": "s", "value": 600},
        {"date": 1413496800, "type": "heart_rate", "unit": "bpm", "value": 150}
    ]}
"""

#todo: map hub-> patient when receiving post Do this tomorrow


#Todo: do something with this waRNING?
#TODO: to fix warning, set timezone. But is the time in utc or should it be converted before setting tzinfo=<UTC> ???

#RuntimeWarning: DateTimeField Measurement.time received a naive datetime (2014-10-16 22:00:00) while time zone support is active.