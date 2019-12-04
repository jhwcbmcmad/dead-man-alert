import time
import futsu.storage
import futsu.fs
import futsu.aws.s3
import tempfile
import boto3
import os.path
import json
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from deadmanalert import VERSION
from deadmanalert.core import server_big_key
from deadmanalert.core import server_clock_prove

def main(ENV_KEY, SOURCE):
    with tempfile.TemporaryDirectory() as tempdir:
        # get timestamp to gen
        t = time.time()
        t += 120
        t //= 3600
        t = int(t)
        t *= 3600
        
        # get server big key
        server_big_key_private_key = server_big_key.get_private_key(ENV_KEY)
        
        # create data
        data = {
            "start"     : t,
            "end"       : t+3600,
        }
        #print(data)
        data_json = json.dumps(
            obj = data,
            separators = (',',':'),
            sort_keys = True,
        )
        
        # create signature
        signature = server_big_key_private_key.sign(
            data = data_json.encode('utf-8'),
            padding = padding.PKCS1v15(),
            algorithm = hashes.SHA256(),
        )

        # signature base64
        signature_b64 = base64.b64encode(signature).decode('utf-8')
        
        # output
        output = {
            "version"   : VERSION,
            "type"      : "clock_prove",
            "clock_prove": {
                "data"      : data_json,
                "source"    : SOURCE,
                "signature" : signature_b64,
            },
        }
        print(output)
        output_json = json.dumps(
            obj = output,
            separators = (',',':'),
            sort_keys = True,
        )
        
        # output to storage
        output_s3_path = server_clock_prove.get_s3_path(ENV_KEY, t)
        print(output_s3_path)
        futsu.storage.bytes_to_path(output_s3_path, output_json.encode('utf-8'))

if __name__ == "__main__":
    import os
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--ENV_KEY', type=str)
    parser.add_argument('--SOURCE', type=str)
    args = parser.parse_args()

    ENV_KEY =   args.ENV_KEY if args.ENV_KEY != None else \
                os.environ['ENV_KEY'] if 'ENV_KEY' in os.environ else \
                None
    SOURCE =    args.SOURCE if args.SOURCE != None else \
                os.environ['SOURCE'] if 'SOURCE' in os.environ else \
                None

    main(
        ENV_KEY = ENV_KEY,
        SOURCE  = SOURCE,
    )
