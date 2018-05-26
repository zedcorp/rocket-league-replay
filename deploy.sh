#!/usr/bin/env bash

echo ">> Update app"
ssh -o "StrictHostKeyChecking no" -tt -i rocketleaguekey.pem ubuntu@34.248.29.223 "cd rocket-league-replay && git pull"

echo ">> Update db"
ssh -o "StrictHostKeyChecking no" -tt -i rocketleaguekey.pem ubuntu@34.248.29.223 "cd rocket-league-replay/rocketleaguereplay && python3 manage.py makemigrations && python3 manage.py migrate"

echo ">> Restart backend"
ssh -o "StrictHostKeyChecking no" -tt -i rocketleaguekey.pem ubuntu@34.248.29.223 "sudo supervisorctl reread && sudo supervisorctl update && sudo supervisorctl restart rlreplay-gunicorn && sudo supervisorctl status"

echo ">> Stop frontend (WIP)"

echo ">> Update frontend dependencies"
ssh -o "StrictHostKeyChecking no" -tt -i rocketleaguekey.pem ubuntu@34.248.29.223 "cd rocket-league-replay/rlrfront && npm install"

echo ">> Start frontend"
ssh -o "StrictHostKeyChecking no" -tt -i rocketleaguekey.pem ubuntu@34.248.29.223 "cd rocket-league-replay/rlrfront && npm start"
