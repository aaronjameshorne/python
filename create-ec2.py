

import os
import boto3
import sys
import traceback

ec2 = boto3.resource('ec2')
imageami = input('Enter AMI Image you want to spin up: ')
string_value = str(imageami)
ami_count = input('number of instances: ')
ami_count_int = int(ami_count)
name_plo = input('policy name: ')
mysg = ec2.create_security_group(GroupName=name_plo,Description='testme')
mysg.authorize_ingress(CidrIp='0.0.0.0/0', IpProtocol='tcp', FromPort=22, ToPort=22)
user_data_packages='''
#!/bin/bash 
sudo yum -y update
sudo yum install -y htop
sudo yum install -y vim
wget -O splunkforwarder-8.0.0-1357bef0a7f6-linux-2.6-x86_64.rpm 'https://www.splunk.com/bin/splunk/DownloadActivityServlet?architecture=x86_64&platform=linux&version=8.0.0&product=universalforwarder&filename=splunkforwarder-8.0.0-1357bef0a7f6-linux-2.6-x86_64.rpm&wget=true'
sudo rpm -i splunkforwarder-8.0.0-1357bef0a7f6-linux-2.6-x86_64.rpm
sudo DD_API_KEY=8b47966137e9f64b6005e591020698e8 bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"
sudo yum install -y git
cd /home/ec2-user/
git clone https://github.com/aaronjameshorne/python.git
sudo yum install epel-release
sudo yum install -y nginx
sudo systemctl start nginx
'''

def default_ami():
    try:
        instances = ec2.create_instances(
            ImageId='ami-0b2d8d1abb76a53d8',
            MinCount=ami_count_int,
            MaxCount=ami_count_int,
            InstanceType='t2.micro',
            NetworkInterfaces=[{'DeviceIndex': 0,'AssociatePublicIpAddress': True,'Groups':[mysg.group_id]}],
            KeyName='webapp',
            UserData=user_data_packages
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
            KeyName='webapp'
    )
    except:
        errorFile = open('aws_log.txt','w')
        errorFile.write(traceback.format_exc())
        errorFile.close()
        print('Any errors will be logged to aws_log file')

if string_value == '':
    default_ami()
else: user_ami()

