import deadmanalert.api.schedule_server_clock_key_rotate as f
import os

def get_var(key, event):
    return  event[key] if key in event else \
            os.environ[key]

def lambda_handler(event, context):
    ENV_KEY = get_var('DMA_ENV_KEY', event)
    SOURCE  = get_var('DMA_SOURCE', event)
    f.main(
        ENV_KEY = ENV_KEY,
        SOURCE  = SOURCE,
    )
