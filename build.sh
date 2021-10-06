#!/bin/sh
sudo docker-compose down
sudo docker image rm scubot_api
sudo docker-compose up -d
sudo docker logs -f go-cqhttp
