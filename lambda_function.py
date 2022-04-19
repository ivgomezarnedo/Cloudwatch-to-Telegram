import json
import cloudwatch_to_telegram


def lambda_handler(event, context):
    lambda_function = event['lambda_function']
    hours = int(event['hours'])
    cloudwatch_to_telegram.main(lambda_function, hours)
    return {
        'statusCode': 200,
        'body': json.dumps('File successfully sent!')
    }


#   lambda_handler(None, None)

