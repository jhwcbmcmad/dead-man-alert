#!/bin/bash

MY_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
PROJECT_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )/../../.." >/dev/null 2>&1 && pwd )"

# create venv for dev
cd ${MY_PATH}
rm -rf venv_dev
python3 -m venv venv_dev
source venv_dev/bin/activate
pip install -r ${MY_PATH}/requirements.txt
deactivate
