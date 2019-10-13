import boto3
import futsu.json
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
import io

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

def create_s3_bucket(env_data):
    ENV_KEY = env_data['ENV_KEY']
    AWS_REGION = env_data['AWS_REGION']

    s3_client = boto3.client('s3',region_name=env_data['AWS_REGION'])
    result = s3_client.list_buckets()
    result = result['Buckets']
    result = map(lambda i:i['Name'], result)
    bucket_name_list = list(result)

    bucket_name = 'dead-man-alert-{ENV_KEY}-perm'.format(ENV_KEY=ENV_KEY)
    if bucket_name not in bucket_name_list:
        s3_client.create_bucket(
            Bucket=bucket_name,
            ACL='private',
            CreateBucketConfiguration={'LocationConstraint':AWS_REGION}
        )

    bucket_name = 'dead-man-alert-{ENV_KEY}-tmp'.format(ENV_KEY=ENV_KEY)
    if bucket_name not in bucket_name_list:
        s3_client.create_bucket(
            Bucket=bucket_name,
            ACL='private',
            CreateBucketConfiguration={'LocationConstraint':AWS_REGION}
        )
        s3_client.put_bucket_lifecycle_configuration(
            Bucket=bucket_name,
            LifecycleConfiguration={
                'Rules': [{
                    'ID': 'expire-delete',
                    'Filter': {'Prefix': ''},
                    'Expiration':{'Days':7},
                    'NoncurrentVersionExpiration':{
                        'NoncurrentDays':7,
                    },
                    'AbortIncompleteMultipartUpload':{
                        'DaysAfterInitiation':3,
                    },
                    'Status':'Enabled',
                }]
            }
        )

def create_server_main_private_key(env_data):
    ENV_KEY = env_data['ENV_KEY']
    AWS_REGION = env_data['AWS_REGION']

    kms_key_alias_name = 'alias/dead-man-alert_{}'.format(ENV_KEY)
    kms_client = boto3.client('kms',region_name=AWS_REGION)
    result = kms_client.list_aliases()
    result = result['Aliases']
    result = filter(lambda i:i['AliasName']==kms_key_alias_name, result)
    result = list(result)
    assert(len(result)==1)
    kms_key_id = result[0]['TargetKeyId']

    bucket_name = 'dead-man-alert-{ENV_KEY}-perm'.format(ENV_KEY=ENV_KEY)
    object_key = 'server/private_key.enc'
    s3_client = boto3.client('s3')
    result = s3_client.list_objects_v2(
        Bucket=bucket_name,
        Prefix=object_key,
    )
    result = result['Contents'] if 'Contents' in result else []
    result = filter(lambda i:i['Key']==object_key, result)
    result = list(result)
    if len(result)==1: return
    assert(len(result)==0)
    
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=4096,
        backend=default_backend(),
    )
    private_key_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    )
    result = kms_client.encrypt(
        KeyId=kms_key_id,
        Plaintext=private_key_bytes
    )
    private_key_bytes_enc = result['CiphertextBlob']
    
    s3_client.upload_fileobj(
        io.BytesIO(private_key_bytes_enc),
        Bucket=bucket_name,
        Key=object_key
    )

def main(env_json_filename):
    env_data = futsu.json.file_to_data(env_json_filename)

    create_kms_key(env_data)
    create_s3_bucket(env_data)
    create_server_main_private_key(env_data)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--env_json', type=str)
    args = parser.parse_args()

    main(env_json_filename=args.env_json)
