import boto3
import json

from get_instance_ebs_details import get_instance_details, get_ebs_details
from tag_instance_ebs import tag_target

region_lookup = {
	"USEA":"us-east-1",
	"USWE":"us-west-1",
	"CACE":"ca-central-1",
	"EUWE":"eu-west-1",
	"EUCE":"eu-cemtral-1",
	"APSP":"ap-southeast-1",
	"APAU":"ap-southeast-2"
}

instance_name = ""
instance_id = ""
target_env = ""
target_ami = ""

target_region = region_lookup[instance_name[:4]]

ec2_data = get_instance_details(instance_name, instance_id, target_env, target_region)
print("EC2 DETAILS DONE")

ebs_data = get_ebs_details(ec2_data, target_env, target_region)
print("EBS DETAILS DONE")
