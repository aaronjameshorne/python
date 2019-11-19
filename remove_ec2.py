import boto3
import time
import sys
import os



rm_nodes():
    list = ['i-0b808541b5ff4e357','i-0fe2703409ed23f55']
    for nodes in list:
    ids = [nodes]
    ec2 = boto3.resource('ec2')
    ec2.instances.filter(InstanceIds = ids).terminate()
    
rm_nodes()
