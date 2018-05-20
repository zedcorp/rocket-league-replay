#!/usr/bin/env bash

ssh -vvv -o "StrictHostKeyChecking no" -tt -i rocketleaguekey.pem ubuntu@34.245.214.229 "cd rocket-league-replay/rocketleaguereplay && pwd && git pull && killall gunicorn ; /usr/local/bin/gunicorn rocketleaguereplay.wsgi --bind 0.0.0.0:8000 --workers=3 --timeout=300"