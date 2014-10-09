from withings import *

access_token = "62c93288933174c5e60c24d3d71bc53d4c51939296cb1f760e036f6355370c"
access_token_secret = "d30ccf3bb4c198deb26762f1d8d2c1d47e5c76d073e4525de2857f751f4266"
consumer_key = "62f96b70bb38711bc7753f94ef78e991e8df4304bd114220ed83b260e43c423"
consumer_secret = "f5c8d22e495d0d24f0d07952ecb5489e711f5dfd315d6fb7d67598532326"
user_id = "4690424"

creds = WithingsCredentials(access_token, access_token_secret, consumer_key, consumer_secret, user_id)

client = WithingsApi(creds)
measures = client.get_measures()
values = {}
values["pulse"] = []
values["ox"] = []
for m in measures:
	pulse = m.get_measure(11)
	ox_sat = m.get_measure(54)
	if pulse != None: 
		values["pulse"].append((pulse, str(m.date)))
	if ox_sat != None: 
		values["ox"].append((ox_sat, str(m.date)))
print values
	
	