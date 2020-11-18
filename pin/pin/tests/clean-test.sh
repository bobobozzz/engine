#!/bin/bash

eval $(docker-machine env testing-server)

target=

while getopts 't:' opts
do
    case $opts in
    t)
        target=$OPTARG
        ;;
    esac
done


if [ "$target" = "" ]; then
    docker-compose -f docker-compose-test.yaml down
    target=test.*pin
else
    docker-compose -f docker-compose-test.yaml rm -sf $target
fi

echo "Clean images match $target..."
docker images -a | grep "$target" | awk '{print $3}' | xargs docker rmi
