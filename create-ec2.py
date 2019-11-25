import os
import boto3
import sys

ec2 = boto3.resource('ec2')

user_data_script = """#!/bin/bash sudo apt install htop"""
imageami = input('Enter AMI Image you want to spin up: ')
string_value = str(imageami)
ami_count = input('number of instances: ')
ami_count_int = int(ami_count)

def default_ami():
    instances = ec2.create_instances(
       ImageId='ami-0dd655843c87b6930',
       MinCount=ami_count_int,
       MaxCount=ami_count_int,
       InstanceType='t2.micro',
       KeyName='webapp',
       UserData=user_data_script
    )

def user_ami():
    instances = ec2.create_instances(
      ImageId=string_value,
      MinCount=ami_count_int,
      MaxCount=ami_count_int,
      InstanceType='t2.micro',
      KeyName='webapp',
      UserData=user_data_script
    )

if string_value == '':
    default_ami()
else: user_ami()
