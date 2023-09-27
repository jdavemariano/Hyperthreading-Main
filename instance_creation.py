import json
import boto3

def create_instance(ec2_data, target_ami, target_region):

    ec2_client = boto3.client('ec2', region_name = target_region)
    
    network_interfaces = []
    for interface in ec2_data['NetworkInterfaces']:
        temp_int = {}

        security_groups = []
        for group in interface['Groups']: 
            security_groups.append(group['GroupId'])

        private_ips = []
        for ipadd in interface['PrivateIpAddresses']:
            target_ip = {'Primary': ipadd['Primary'],'PrivateIpAddress': ipadd['PrivateIpAddress']}
            private_ips.append(target_ip)


        temp_int = {
            'SubnetId': interface['SubnetId'],
            'DeviceIndex': interface['Attachment']['DeviceIndex'],
            'DeleteOnTermination': interface['Attachment']['DeleteOnTermination'],
            'Description': interface['Description'],
            'Groups': security_groups,
            'PrivateIpAddresses': private_ips,
            'InterfaceType': interface['InterfaceType'] ,
            'NetworkCardIndex': interface['Attachment']['NetworkCardIndex'],
        }

        network_interfaces.append(temp_int)

    monitoring_stat = True
    if ec2_data['Monitoring']['State'] == "disabled":
      monitoring_stat = False

    print(private_ips)

    instances = ec2_client.run_instances(
        ImageId=target_ami,
        KeyName=ec2_data['KeyName'],
        InstanceType = ec2_data['InstanceType'],
        MaxCount=1,
        MinCount=1,
        Monitoring={'Enabled': monitoring_stat},
        Placement=ec2_data['Placement'],
        DisableApiTermination=True,
        EbsOptimized=ec2_data['EbsOptimized'],
        IamInstanceProfile={'Arn': ec2_data['IamInstanceProfile']['Arn']},
        InstanceInitiatedShutdownBehavior="stop",
        NetworkInterfaces=network_interfaces,
        CpuOptions={
                'CoreCount': ec2_data['CpuOptions']['CoreCount'],
                'ThreadsPerCore': 1,
        },
        HibernationOptions=ec2_data['HibernationOptions'],
        #PrivateDnsNameOptions=ec2_data['PrivateDnsNameOptions']
    )

    return(instances["Instances"][0]["InstanceId"])
