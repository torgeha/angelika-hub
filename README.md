angelika-hub
============

Scripts to be run on the hub for project Angelika - health tracking.

[Backend](https://github.com/sigurdsa/angelika-api/) and [frontend](https://github.com/iver56/angelika-web) is in separate repositories.

## Setup

### Setup hub with the [Withings Pulse](http://www.withings.com/eu/withings-pulse.html).
* `cd withings/`
* `python setup.py install`
* Make sure to create directories `res/` and `cache/` inside the `hub/` directory. 
* In `res/` create `oauth_pulseO2.txt` with this structure:

   [keys]  
   consumer_key=  
   consumer_secret=  
   oauth_token=  
   oauth_token_secret=  
   user_id=  

* In `res/` `create hub_config.txt`.

Everything should now work, run `hub.py`
