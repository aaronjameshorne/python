import boto3
import time
import sys
import os

def disable_vm():
    ids = ['i-00c0fb8e8c41a90e1']
    ec2 = boto3.resource('ec2')
    ec2.instances.filter(InstanceIds = ids).terminate()

disable_vm()
