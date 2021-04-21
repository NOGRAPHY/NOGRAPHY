import json

ENCODING_DECODING_BASE = 3

def lambda_handler(event, context):
    secret = event['secret'].strip()
    placeholder = event['placeholder'].strip()
    show_colors = event['show_colors']

    if len(secret) * ENCODING_DECODING_BASE > len(placeholder):
        return {
            "statusCode": 400,
            "error": "Secret is too long. Make it shorter or the placeholder longer."
            }
    else:
        # TODO
        return {
            "statusCode": 200,
            "body": secret
        }