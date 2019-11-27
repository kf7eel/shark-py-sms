# shark-py-sms

----

Place these files in the same folder as the shark-py files. shark-py must be the version here (https://github.com/kf7eel/shark-py) to work these scripts.
This will work with Openspot firmware 0101 or later as all versions after 0101 use JSON Web Tokens.


----

### noaa.py - NWS Weather Alert to SMS
This script will check for moderate, severe, or extreme weather alerts and send them to the configured sms receiver.
Setting this up to send to a talk group will allow multiple users to receive severe weather alerts.

Requires the python module WeatherAlerts. https://weatheralerts.readthedocs.io/en/latest/about.html
