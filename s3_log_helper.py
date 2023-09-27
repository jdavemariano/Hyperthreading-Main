import boto3
import json
import os
from datetime import datetime   

def write_json_s3(filename, folder):
    log_file = open(filename)
    log_json = log_file.read()
    log_json = log_json.replace("'",'"')
    log_json = json.loads(log_json)
    instance_name = os.environ['Instance Name']
    
    target_bucket = "hyper-threading-automation-logs"
    target_date = str(datetime.today().strftime('%Y-%m-%d(%H:%M:%S)'))
    final_filename = f'{filename}({target_date}).json'

    s3_resource = boto3.resource('s3')
    folder_filename = f'{folder}/{final_filename}'
    s3object = s3_resource.Object(target_bucket, folder_filename)
    s3object.put(Body=(bytes(json.dumps(log_json, indent=4).encode('UTF-8'))))

write_json_s3(f'{instance_name}-ec2_details.json', "ec2-details-log")
write_json_s3(f'{instance_name}-ebs_details.json', "ebs-details-log")
