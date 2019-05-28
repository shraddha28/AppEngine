#!/bin/bash

curl "http://localhost:8080/"
sleep 2
curl "http://localhost:8080/blend/"
sleep 2
curl -d "_name=&param2=value2" -X POST http://localhost:3000/data
