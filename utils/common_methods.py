import configparser

config_file = configparser.ConfigParser()
config_file.read("config.properties", encoding='latin-1')

TELEGRAM_TOKEN = config_file.get("prod.TELEGRAM", "TOKEN")
TELEGRAM_METRICS_GROUP_ID = config_file.get("prod.TELEGRAM", "METRICS_GROUP_ID")

AWS_ID = config_file.get("prod.AWS", "AWS_ID")
AWS_KEY = config_file.get("prod.AWS", "AWS_KEY")
AWS_REGION = config_file.get("prod.AWS", "AWS_REGION")