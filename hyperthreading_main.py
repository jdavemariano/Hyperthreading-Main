import boto3
import json

from get_instance_ebs_details import get_instance_details, get_ebs_details
from tag_instance_ebs import tag_target
from instance_creation import create_instance
from instance_termination import terminate_instance

region_lookup = {
	"USEA":"us-east-1",
	"USWE":"us-west-1",
	"CACE":"ca-central-1",
	"EUWE":"eu-west-1",
	"EUCE":"eu-cemtral-1",
	"APSP":"ap-southeast-1",
	"APAU":"ap-southeast-2"
}

instance_name = "USEAPDAJ3DB23"
instance_id = "i-074c96dc9af6a26a0"
target_env = "dco"
target_ami = "ami-01ec1239b9dabe1e4"

target_region = region_lookup[instance_name[:4]]

ec2_data = get_instance_details(instance_name, instance_id, target_env, target_region)
print("EC2 DETAILS DONE")

ebs_data = get_ebs_details(ec2_data, target_env, target_region)
print("EBS DETAILS DONE")

#terminate_instance(instance_id, target_ami, target_env, target_region)

#new_instance_id = create_instance(ec2_data, target_ami, target_env, target_region)
print(new_instance_id)

#tag_target(instance_name, new_instance_id, ec2_data, ebs_data, target_region, target_env)
print("TAGS DONE")
