import json
import os
import cloudwatch_to_telegram


def lambda_handler(event, context):
    lambda_function = os.environ['lambda_function']
    hours = int(os.environ['hours'])
    cloudwatch_to_telegram.main(lambda_function, hours)
    return {
        'statusCode': 200,
        'body': json.dumps('File successfully sent!')
    }


#event = {'lambda_function': 'YOUR_AWS_LAMBDA_FUNCTION_NAME', 'hours': '20'}
#lambda_handler(event, None)
