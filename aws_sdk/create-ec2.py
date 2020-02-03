import os
import boto3
import sys
import traceback
import time
import pyperclip
import user_data


ec2 = boto3.resource('ec2')
imageami = input('Enter AMI Image you want to spin up: ')
string_value = str(imageami)
ami_count = input('number of instances: ')
ami_count_int = int(ami_count)
name_plo = input('policy name: ')
mysg = ec2.create_security_group(GroupName=name_plo,Description='testme')
mysg.authorize_ingress(IpPermissions=[
            {'IpProtocol': 'tcp',
             'FromPort': 80,
             'ToPort': 80,
             'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
            {'IpProtocol': 'tcp',
             'FromPort': 22,
             'ToPort': 22,
             'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
        ])


def default_ami():
    try:
        instances = ec2.create_instances(
            ImageId='ami-0b2d8d1abb76a53d8',
            MinCount=ami_count_int,
            MaxCount=ami_count_int,
            InstanceType='t2.micro',
            NetworkInterfaces=[{'DeviceIndex': 0,'AssociatePublicIpAddress': True,'Groups':[mysg.group_id]}],
            KeyName='raspberry_pi',
            UserData=user_data.user_data_packages
    )
    except:
        errorFile = open('aws_log.txt','w')
        errorFile.write(traceback.format_exc())
        errorFile.close()
        print('Any errors will be logged to aws_log file')
def user_ami():
    try:
        instances = ec2.create_instances(
            ImageId=string_value,
            MinCount=ami_count_int,
            MaxCount=ami_count_int,
            InstanceType='t2.micro',
            NetworkInterfaces=[{'DeviceIndex': 0,'AssociatePublicIpAddress': True,'Groups':[mysg.group_id]}],
            KeyName='raspberry_pi'
    )
    except:
        errorFile = open('aws_log.txt','w')
        errorFile.write(traceback.format_exc())
        errorFile.close()
        print('Any errors will be logged to aws_log file')

if string_value == '':
    default_ami()
else: user_ami()
print('Wait for IPs to be return to connect.')
time.sleep(40)
os.system('python3 info_ec2.py | grep Public | grep -v DnsName | grep -v Address')

