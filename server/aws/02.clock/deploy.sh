#!/bin/bash

set -e

MY_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
PROJECT_PATH="$( cd "$( dirname "${MY_PATH}" )/../.." >/dev/null 2>&1 && pwd )"

if [[ $# -ne 1 ]]; then
    echo "${0} _env_"
    exit 1
fi

ENV_NAME=${1}
ENV_JSON=${PROJECT_PATH}/env/${ENV_NAME}/env.json
ENV_KEY=`cat ${ENV_JSON} | jq -r .ENV_KEY`

TIMESTAMP=`date +%s`

rm -rf /tmp/CSXAHBIAFL-*
TMP_PATH=/tmp/CSXAHBIAFL-${TIMESTAMP}
mkdir -p ${TMP_PATH}

# create venv for lambda runtime
cd ${TMP_PATH}
rm -rf venv_runtime
python3 -m venv venv_runtime
source venv_runtime/bin/activate
pip install --upgrade pip
pip install --upgrade -r ${MY_PATH}/requirements.txt
deactivate

# create lambda package
cd ${TMP_PATH}
rm -rf ${TMP_PATH}/build
mkdir -p ${TMP_PATH}/build
cd ${TMP_PATH}/venv_dev/lib/python3.7/site-packages
zip -r9 ${TMP_PATH}/build/lambda.zip .
cd ${MY_PATH}/lambda
zip -g ${TMP_PATH}/build/lambda.zip lambda_handler.py
zip -g ${TMP_PATH}/build/lambda.zip main.py

# create venv for deploy
cd ${TMP_PATH}
rm -rf venv_deploy
python3 -m venv venv_deploy
source venv_deploy/bin/activate
pip install --upgrade pip
pip install --upgrade awscli

# create role
aws iam create-role \
    --role-name dead_man_alert_${ENV_KEY}_clock \
    --assume-role-policy-document

# create new lambda function
cd ${TMP_PATH}
aws lambda create-function \
    --function-name dead_man_alert_${ENV_KEY}_clock \
    --runtime python3.7 \
    --role arn:${AWS_IAM_ROLE_ARN} \
    --handler lambda_handler.lambda_handler \
    --zip-file fileb://build/lambda.zip

deactivate
