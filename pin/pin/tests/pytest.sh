#!/usr/bin/env sh

#BoBoBo#

target=.
allnew=0
justenv=0

while getopts 'ent:' opts
do
    case $opts in
    e)
        justenv=1;;
    n)
        allnew=1;;
    t)
        target=$OPTARG;;
    esac
done


curdir=`pwd`
basedir=$(cd "$(dirname "$0")"; pwd)
echo "Go to test base dir : ${basedir}"
cd ${basedir}

if [  -d test-venv ]; then
    if [ ${allnew} -eq 1 ]; then
        rm -rf test-venv
        python3 -m venv test-venv
        source ./test-venv/bin/activate
        pip install -r ../../test-requirements.txt
    fi
else
    python3 -m venv test-venv
    source ./test-venv/bin/activate
    pip install -r ../../test-requirements.txt
fi

echo "export PIN_CONF=${basedir}/pin.conf" >> ./test-venv/bin/activate
echo "export PYTHONPATH=${PYTHONPATH}:${basedir}/../.." >> ./test-venv/bin/activate

source ./test-venv/bin/activate
if [ ${justenv} -eq 0 ]; then
    echo "Starting to run pytest to : $target"
    pytest -s $target
fi

echo "Go back to dir : ${curdir}"
cd $curdir
