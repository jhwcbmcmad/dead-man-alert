import boto3
import futsu.json

def create_kms_key(env_data):
    key_alias_name = 'alias/dead-man-alert_{}'.format(env_data['ENV_KEY'])

    kms_client = boto3.client('kms',region_name=env_data['AWS_REGION'])
    
    result = kms_client.list_aliases()
    result = result['Aliases']
    result = filter(lambda i:i['AliasName']==key_alias_name, result)
    result = list(result)
    key_id = result[0]['TargetKeyId'] if (len(result)==1) else None
    
    if key_id == None:
        result = kms_client.create_key(
            Description=key_alias_name
        )
        key_id = result['KeyMetadata']['KeyId']
        kms_client.create_alias(
            AliasName=key_alias_name,
            TargetKeyId=key_id
        )

def main(env_json_filename):
    env_data = futsu.json.file_to_data(env_json_filename)

    create_kms_key(env_data)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--env_json', type=str)
    args = parser.parse_args()

    main(env_json_filename=args.env_json)
