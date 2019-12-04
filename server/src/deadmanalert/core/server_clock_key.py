from deadmanalert import VERSION

def get_private_key_s3_path(ENV_KEY, t):
    t_str = str(t)
    s3_path = 's3://dead-man-alert-{ENV_KEY}-tmp/{VERSION}/server/clock_key/{t0}/{t1}/{t}/clock_private_key.pem'.format(
        ENV_KEY=ENV_KEY,
        VERSION = VERSION,
        t0 = t_str[:-7],
        t1 = t_str[-7:-5],
        t  = t_str,
    )
    return s3_path

def get_public_key_cert_s3_path(ENV_KEY, t):
    t_str = str(t)
    s3_path = 's3://dead-man-alert-{ENV_KEY}-tmp/{VERSION}/server/clock_key/{t0}/{t1}/{t}/clock_public_key_cert.json'.format(
        ENV_KEY=ENV_KEY,
        VERSION = VERSION,
        t0 = t_str[:-7],
        t1 = t_str[-7:-5],
        t  = t_str,
    )
    return s3_path
