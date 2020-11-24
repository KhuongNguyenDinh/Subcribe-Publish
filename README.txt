$ pip install flask-mqtt

from flask import Flask
from flask_mqtt import Mqtt

To subcribe:
To subscribe to a topic simply use `mqtt.subscribe()`. To make sure the
subscription gets handled correctly on startup place the subscription inside
an `on_connect()` callback function.

to run:
flask run
-
goto localhost
