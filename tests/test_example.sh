#!/usr/bin/env sh

#BoBoBo#

echo "Start cleaning..."
docker-compose down
echo "Cleaned all."

docker-compose up -d test-example-helloworld
docker logs -f engine.test.example.helloworld

echo "Start cleaning..."
#docker-compose down
echo "Cleaned all."
