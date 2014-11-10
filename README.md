angelika-hub
============

Scripts to be run on the hub for project Angelika - health tracking.

[Backend](https://github.com/sigurdsa/angelika-api/) and [frontend](https://github.com/iver56/angelika-web) is in separate repositories.

## Setup

### Setup hub with the [Withings Pulse](http://www.withings.com/eu/withings-pulse.html).
* Create a virtual environment: `virtualenv env`
* Activate it: `. env/bin/activate`
* `python setup.py install`
* `cd withings/`
* `python setup.py install`
* In `res/` create `oauth_pulseO2.txt` with this structure:

   [keys]  
   consumer_key=  
   consumer_secret=  
   oauth_token=  
   oauth_token_secret=  
   user_id=  

When running `hub.py` for the first time, the prompt will ask for configuration information. This can be edited later in `res/hub_config.txt`.
