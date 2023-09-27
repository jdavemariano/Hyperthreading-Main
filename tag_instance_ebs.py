import boto3
import json

def tag_target(instance_name, instance_id, ec2_data, ebs_data, target_region, target_env):
	api_keys_file = open("api_keys.json")
	api_keys = json.load(api_keys_file)

	ec2_client = boto3.client('ec2', region_name = target_region, aws_access_key_id=api_keys[target_env]['key'], aws_secret_access_key=api_keys[target_env]['secret'])
	ec2_details = ec2_client.describe_instances(InstanceIds=[instance_id])
	ec2_details = ec2_details["Reservations"][0]["Instances"][0]

	instance_tags = ec2_data['Tags']

	#instance tags
	instance_tag_response = ec2_client.create_tags(Resources=[instance_id], Tags=instance_tags)

	#ebs tags
	for dev in ebs_data:

		for device in ec2_details['BlockDeviceMappings']:
			if device['DeviceName'] == dev:
				vol_id = device['Ebs']['VolumeId']

		vol_tags = ebs_data[dev]
		ebs_tag_response = ec2_client.create_tags(Resources=[vol_id], Tags=vol_tags)

	return(instance_tag_response, ebs_tag_response)
