
import requests
import json


class JsonPosting:

    def post_file(self, file_to_post, username, password, server_url=None, token=None):
        """
        Tries to authenticate based on username/password if token is not provided.
        Posts provided file to API. THROES EXCEPTION! Must be handled!
        """

        if not server_url:
            print "No server_url provided"
            raise requests.ConnectionError

        # If no token is given, username and password is needed to provide new token
        if not token:
            token = self.authenticate(username, password, server_url)

        with open(file_to_post) as json_file:

            # Get the json data from file
            payload = json.load(json_file)

            # url = "http://127.0.0.1:8000/post-measurements/" # Remember trailing slash
            url = server_url

            headers = {'content-type': 'application/json', 'Authorization': "Token " + token}

            r = requests.post(url, data=json.dumps(payload), headers=headers)
            print "Boyz in da hood"

            print r.status_code
            print r.text

            self.raise_exception_if_bad_request(r)

        return token

    def authenticate(self, username, password, server_url):
        """
        Tries to authenticate the hub based on username and password. Raises exception if response status code is not
        2xx. I.e username or password is wrong or serverside error.
        """

        # url = "http://127.0.0.1:8000/api-token-auth/" # Remember trailing slash
        url = server_url


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