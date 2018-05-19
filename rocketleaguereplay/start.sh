#!/bin/bash

/usr/local/bin/gunicorn rocketleaguereplay.wsgi --bind 0.0.0.0:8000
