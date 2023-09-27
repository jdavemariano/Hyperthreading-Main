import boto3
import json

def terminate_instance(server_id, ami_id, target_region):
    ec2_client = boto3.client('ec2', region_name=target_region)
    ami_waiter = ec2_client.get_waiter('image_available')

    #instance state check
    response_server = ec2_client.describe_instances(InstanceIds=[server_id])
    state_server = response_server['Reservations'][0]['Instances'][0]['State']['Name']

    #ami state check
    response_ami = ec2_client.describe_images(ImageIds=[ami_id])
    state_ami = response_ami['Images'][0]['State']

    if state_ami == 'available':
        print("The ami is now available")
        if state_server == 'stopped':
            print("The server is on stopped state")
            
            #termination protection disabling
            ec2_client.modify_instance_attribute(InstanceId=server_id,Attribute="disableApiTermination",Value="False")
            print("Termination Protection is now disabled")
            
            #actual termination of the server
            ec2_client.terminate_instances(InstanceIds=[server_id])
            print("Server has been terminated")
            
            #instance termination waiter
            instance_waiter = ec2_client.get_waiter('instance_terminated')
            instance_waiter.wait(InstanceIds=[server_id], WaiterConfig={'Delay': 30,'MaxAttempts': 60})

        elif state_server == 'running':
            print("Server should be on stopped state aborting")
            exit()
        else:
            print("Server Condition State Not Met")
            exit()

    if state_ami == 'pending':
        print("The ami is not yet available")
        
        #Waiter for AMI completion
        ami_waiter.wait(ImageIds=[ami_id], WaiterConfig={'Delay': 30,'MaxAttempts': 60})
        print("The AMI is now available")
