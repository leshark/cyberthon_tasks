#!/bin/sh

ES_URL="http://127.0.0.1:9200"


for i in {1..137}
do
	curl -XPUT -H 'Content-Type: application/json' "$ES_URL/flag/post/$i?pretty" -d'
    {
    "title": "Flag may be here",
    "content": "well, not here"
    }' &> /dev/null
done

curl -XPUT -H 'Content-Type: application/json' "$ES_URL/flag/post/138?pretty" -d'
{
  "title": "Flag may be here",
  "content": "HERE: CYBERTHON{Se3c4_ev3yDa8}"
}' &> /dev/null


for i in {139..150}
do
	curl -XPUT -H 'Content-Type: application/json' "$ES_URL/flag/post/$i?pretty" -d'
    {
    "title": "Flag may be here",
    "content": "well, not here"
    }' &> /dev/null
done

curl -XPUT -H 'Content-Type: application/json'  "$ES_URL/flag/_settings" -d'
{
  "index": {
    "blocks.read_only": true
  }
}'

# curl -XPOST -H 'Content-Type: application/json'  "$ES_URL/flag/_close"