import boto3
from datetime import datetime, timedelta
from utils import telegram_methods, common_methods


def get_log_events(log_group, aws_client, start_time=None, end_time=None):
    """Generate all the log events from a CloudWatch group.
    Args:
        log_group: Name of the CloudWatch log group.
        aws_client: boto3 client for CloudWatch.
        start_time: Only fetch events with a timestamp after this time.
            Expressed as the number of milliseconds after midnight Jan 1 1970.
        end_time: Only fetch events with a timestamp before this time.
            Expressed as the number of milliseconds after midnight Jan 1 1970.

    """
    kwargs = {
        'logGroupName': log_group,
        'limit': 10000,
    }

    if start_time is not None:
        kwargs['startTime'] = start_time
    if end_time is not None:
        kwargs['endTime'] = end_time

    while True:
        resp = aws_client.filter_log_events(**kwargs)
        yield from resp['events']
        try:
            kwargs['nextToken'] = resp['nextToken']
        except KeyError:  # no more pages
            break


def get_start_time(hours_since):
    """
    Get the start time from which start downloading logs.
    Returns:
        start_time: The start time in milliseconds after midnight Jan 1 1970.
    """
    d = datetime.utcnow() - timedelta(hours=hours_since)
    start_time = int(datetime.timestamp(d) * 1000)
    return start_time


def write_to_file(log_text, file_path):
    """
    Write the log text to a file.
    Args:
        log_text:  The log text to write to the file.
        file_path:  The path of the file to write to.

    Returns:
        None
    """
    with open(file_path, "w") as text_file:
        text_file.write(log_text)


def main(log_group, hours_since):
    client = boto3.client(
        'logs',
        aws_access_key_id=common_methods.AWS_ID,
        aws_secret_access_key=common_methods.AWS_KEY,
        region_name=common_methods.AWS_REGION
    )
    start_time = get_start_time(hours_since)
    log_text = ""
    print("Downloading logs from CloudWatch...")
    for x in get_log_events(log_group=log_group, aws_client=client, start_time=start_time):
        log_text = log_text + x['message']
    file_name = f"{str(datetime.now())[0:19].replace(' ','_').replace(':','_')}_logs.txt"
    file_path = "/tmp/" + file_name  # tmp is the only writable folder in AWS Lambda
    print(f"Writing logs to file {file_path}")
    write_to_file(log_text, file_path)
    print("Uploading logs to Telegram...")
    telegram_methods.send_document_to_telegram(file_path, file_name)

