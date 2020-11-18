#!/bin/bash

eval $(docker-machine env testing-server)

target=
clean=0

while getopts 't:c' opts
do
    case $opts in
    t)
        target=$OPTARG
        ;;
    c)
        clean=1
        ;;
    esac
done

if [ $clean -eq 1 ]; then
    echo "Start cleaning..."
    ./clean-test.sh -t $target
    echo "Cleaned all."
fi

docker-compose -f docker-compose-test.yaml up -d $target
