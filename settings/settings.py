import os

SMS_URL = os.environ['SMS_URL'] if 'SMS_URL' in os.environ else 'https://smsapi.sms.com/cgi-bin/smsgateway'
SMS_SERVICE_NAME = os.environ['SMS_SERVICE_NAME'] if 'SMS_SERVICE_NAME' in os.environ else 'sms_service'
SMS_PHONES = [ phone.strip() for phone in os.environ['SMS_PHONES'].split(',') ] if 'SMS_PHONES' in os.environ else []
