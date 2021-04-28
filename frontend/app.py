import json


def lambda_handler(event, context):
    print(event)
    
    template = open('./templates/hide.html', "r").read()

    return {
        "statusCode": 200,
        "headers": {'Content-Type': 'text/html'},
        "body": template
    }
