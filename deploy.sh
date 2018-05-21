#!/usr/bin/env bash

echo ">> Update app"
ssh -v -o "StrictHostKeyChecking no" -tt -i rocketleaguekey.pem ubuntu@34.248.29.223 "cd rocket-league-replay && git pull"

echo ">> Update db"
ssh -v -o "StrictHostKeyChecking no" -tt -i rocketleaguekey.pem ubuntu@34.248.29.223 "cd rocket-league-replay/rocketleaguereplay && python3 manage.py makemigrations && python3 manage.py migrate"

echo ">> Restart"
ssh -v -o "StrictHostKeyChecking no" -tt -i rocketleaguekey.pem ubuntu@34.248.29.223 "sudo supervisorctl reread && sudo supervisorctl update && sudo supervisorctl restart rlreplay-gunicorn && sudo supervisorctl status"
