#!/usr/bin/env bash

ssh -vvv -o "StrictHostKeyChecking no" -tt -i rocketleaguekey.pem ubuntu@34.245.214.229 "cd rocket-league-replay && pwd && git pull && sudo supervisorctl reread && sudo supervisorctl update && sudo supervisorctl restart rlreplay-gunicorn && sudo supervisorctl status"
