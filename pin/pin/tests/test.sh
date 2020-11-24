#!/bin/bash

target=
clean=1

while getopts 't:r' opts
do
    case $opts in
    t)
        target=$OPTARG
        ;;
    r)
        clean=0
        ;;
    esac
done

clean(){
    if [ $clean -eq 1 ]; then
        echo "Start cleaning..."
        docker-compose -f docker-compose-test.yaml down
        echo "Cleaned all."
    fi
}

clean
docker-compose -f docker-compose-test.yaml up -d $target
echo "Waiting..."
sleep 5
docker logs -f engine.test.pin
clean
