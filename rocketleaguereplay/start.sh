#!/bin/bash

killall gunicorn
/usr/local/bin/gunicorn rocketleaguereplay.wsgi --bind 0.0.0.0:8000 -workers=3 --timeout=300
