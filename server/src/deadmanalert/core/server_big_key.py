import boto3
import futsu.storage
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

def get_private_key(ENV_KEY):
    # get private key enc binary
    private_key_s3_path = 's3://dead-man-alert-{ENV_KEY}-perm/server/private_key.enc'.format(ENV_KEY=ENV_KEY)
    private_key_bytes_enc = futsu.storage.path_to_bytes(private_key_s3_path)

    # decrypt private key binary
    kms_client = boto3.client('kms')
    decrypt_result = kms_client.decrypt(CiphertextBlob=private_key_bytes_enc)
    private_key_bytes = decrypt_result['Plaintext']
    
    # load private key
    private_key = serialization.load_pem_private_key(
        private_key_bytes,
        password=None,
        backend=default_backend(),
    )
    return private_key
