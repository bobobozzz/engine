if [  -d test-venv ]; then
    rm -rf test-venv
    python -m venv test-venv
else
    python -m venv test-venv
fi

source ./test-venv/bin/activate
pip install -r ./test-requirements.txt
