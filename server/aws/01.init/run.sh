#!/bin/bash

set -e

MY_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
PROJECT_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )/../../.." >/dev/null 2>&1 && pwd )"

if [[ $# -ne 1 ]]; then
    echo "${0} _env_"
    exit 1
fi

ENV_NAME=${1}
ENV_JSON=${PROJECT_PATH}/env/${ENV_NAME}/env.json

TIMESTAMP=`date +%s`

rm -rf /tmp/CSXAHBIAFL-*
TMP_PATH=/tmp/CSXAHBIAFL-${TIMESTAMP}
mkdir -p ${TMP_PATH}

# create venv for aws
cd ${TMP_PATH}
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install --upgrade -r ${MY_PATH}/requirements.txt

python3 ${MY_PATH}/_run.py \
    --env_json=${ENV_JSON}

deactivate

cd /
rm -rf /tmp/CSXAHBIAFL-*
