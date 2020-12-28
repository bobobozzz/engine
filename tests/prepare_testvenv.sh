if [  -d test-venv ]; then
    rm -rf test-venv
    python3 -m venv test-venv
else
    python3 -m venv test-venv
fi

source ./test-venv/bin/activate
pip3 install -r ./test-requirements.txt
