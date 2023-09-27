eimport boto3
import json
from datetime import datetime	

def write_json_s3():
	log_file = open("sample_data.json")
	log_json = log_file.read()
	log_json = log_json.replace("'",'"')
	log_json = json.loads(log_json)

	target_bucket = "hyper-threading-automation-logs"
	target_date = str(datetime.today().strftime('%Y-%m-%d(%H:%M:%S)'))
	final_filename = f'ec2-details({target_date}).json'

	s3_resource = boto3.resource('s3')
	folder_filename = f'ec2-details-log/{final_filename}'
	s3object = s3_resource.Object(target_bucket, folder_filename)

	s3object.put(Body=(bytes(json.dumps(log_json, indent=4).encode('UTF-8'))))

write_json_s3()
