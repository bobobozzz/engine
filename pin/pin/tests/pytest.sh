#!/usr/bin/env sh

#BoBoBo#

target=.

while getopts 't:' opts
do
    case $opts in
    t)
        target=$OPTARG;;
    esac
done

echo "Starting to run pytest to : $target"

curdir=`pwd`
basedir=$(cd "$(dirname "$0")"; pwd)
echo "Go to test base dir : ${basedir}"
cd ${basedir}

if [  -d test-venv ]; then
    rm -rf test-venv
    python3 -m venv test-venv
else
    python3 -m venv test-venv
fi

echo "export PYTHONPATH=${PYTHONPATH}:~/code/servs/suser" >> ./test-venv/bin/activate

source ./test-venv/bin/activate
pip install -r ../../test-requirements.txt

export PIN_CONF=${curdir}/pin.conf
pytest -s $target

echo "Go back to dir : ${curdir}"
cd $curdir
