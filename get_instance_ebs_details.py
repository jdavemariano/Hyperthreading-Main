from datetime import datetime
import boto3
import json


#def write_json_s3(target_filename, json_data, target_folder=""):
#	target_env = "goss"
#	target_bucket = "hyper-threading-automation-logs"
#	target_date = str(datetime.today().strftime('%Y-%m-%d(%H:%M)'))
#	final_filename = f'{target_filename}({target_date}).json'

#	s3_resource = boto3.resource('s3', aws_access_key_id=api_keys[target_env]['key'], aws_secret_access_key=api_keys[target_env]['secret'])
#	folder_filename = f'{target_folder}{final_filename}'
#	s3object = s3_resource.Object(target_bucket, folder_filename)

#	s3object.put(Body=(bytes(json.dumps(json_data, indent=4).encode('UTF-8'))))

def get_instance_details(instance_name, instance_id, target_region):
	ec2_client = boto3.client('ec2', region_name = target_region)
	response = ""

	try:
		response = ec2_client.describe_instances(InstanceIds=[instance_id])
	except Exception as e:
		if "does not exist" in str(e):
			return("The instance ID does not exist")

	if response:
		instance_details = response["Reservations"][0]["Instances"][0]

		instance_details['LaunchTime'] = str(instance_details['LaunchTime'])
		instance_details['UsageOperationUpdateTime'] = str(instance_details['UsageOperationUpdateTime'])

		counter = 0
		for item in instance_details['BlockDeviceMappings']:
			instance_details['BlockDeviceMappings'][counter]['Ebs']['AttachTime'] = str(instance_details['BlockDeviceMappings'][counter]['Ebs']['AttachTime'])
			counter += 1

		counter = 0
		for item in instance_details['NetworkInterfaces']:
			instance_details['NetworkInterfaces'][counter]['Attachment']['AttachTime'] = str(instance_details['NetworkInterfaces'][counter]['Attachment']['AttachTime'])
			counter += 1

#	filename = f'{instance_name}_ec2'
#	write_json_s3(filename, instance_details, "ec2-details-log/")

	with open('ec2_details.json', 'w') as f:
    	json.dump(instance_details, f)
		
	return(instance_details)

def get_ebs_details(ec2_data, target_region):
	ec2_client = boto3.client('ec2', region_name = target_region)
	vol_tags = {}

	for vol in ec2_data['BlockDeviceMappings']:
		device_name = vol['DeviceName']
		volume_id = vol['Ebs']['VolumeId']
		response = ec2_client.describe_volumes(VolumeIds=[volume_id])
		
		if "Tags" in response['Volumes'][0].keys():
			vol_tags[device_name] = response['Volumes'][0]['Tags']

			for tag in ec2_data['Tags']:
				if tag['Key'] == "Name":
					instance_name = tag['Value']

#			filename = f'{instance_name}_ebs'
#			write_json_s3(filename, vol_tags, "ebs-details-log/")

	return(vol_tags)
