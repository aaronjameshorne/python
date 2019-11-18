import os
import boto3
import sys




ec2 = boto3.resource('ec2')

imageami = input('Enter AMI Image you want to spin up: ')
string_value = str(imageami)
ami_count = input('number of instances: ')
ami_count_int = int(ami_count)


def default_ami():
    instances = ec2.create_instances(
        ImageId='ami-00fc224d9834053d6',
        MinCount=ami_count_int,
        MaxCount=ami_count_int,
        InstanceType='t2.micro',
        KeyName='webapp'
    )

def user_ami():
    instances = ec2.create_instances(
      ImageId=string_value,
      MinCount=ami_count_int,
      MaxCount=ami_count_int,
      InstanceType='t2.micro',
      KeyName='webapp'
    )

if string_value == '':
    default_ami()
else: user_ami()
