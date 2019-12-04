# deadmanalert

## test

```
export DMA_ENV_NAME=dev

python3 -m venv venv-test
source venv-test/bin/activate
pip install boto3 futsu cryptography

export DMA_ENV_KEY=`cat ../../env/${DMA_ENV_NAME}/env.json | jq -r .ENV_KEY`
export DMA_SOURCE=`cat ../../env/${DMA_ENV_NAME}/env.json | jq -r .SOURCE`
export AWS_DEFAULT_REGION=`cat ../../env/${DMA_ENV_NAME}/env.json | jq -r .AWS_REGION`
export DMA_VERSION=`python3 -m deadmanalert.version`

python3 -m deadmanalert.api.schedule_server_clock_key_rotate
python3 -m deadmanalert.api.schedule_server_clock_prove_rotate
```

## upload

```
python3 -m venv venv-upload
source venv-upload/bin/activate

pip install --upgrade setuptools wheel nose twine keyring

rm -rf dist
python3 setup.py sdist bdist_wheel

python3 -m twine upload -u 6SXXzi4kEcjpHaiF --repository-url https://test.pypi.org/legacy/ dist/*
python3 -m twine upload -u okzV57CEeP8FqwJQ dist/*
deactivate
```
