#!/bin/bash

echo "Start cleaning..."
docker-compose down
echo "Cleaned all."

docker-compose up -d
echo "Waiting..."
sleep 5
docker logs -f engine.test.pin

echo "Start cleaning..."
docker-compose down
echo "Cleaned all."
