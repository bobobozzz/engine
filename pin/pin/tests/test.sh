#!/bin/bash

echo "Start cleaning..."
docker-compose -f docker-compose-test.yaml down
echo "Cleaned all."

docker-compose -f docker-compose-test.yaml up -d
echo "Waiting..."
sleep 5
docker logs -f engine.test.pin

echo "Start cleaning..."
docker-compose -f docker-compose-test.yaml down
echo "Cleaned all."
