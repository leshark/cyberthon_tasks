#!/bin/sh

docker stop elasticsearch && 
docker rm elasticsearch &&
docker run -d --name elasticsearch  -p 9200:9200 --memory="4g" -e "discovery.type=single-node" elasticsearch:7.10.1 &&
echo started elastic!