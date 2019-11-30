import boto3
import pprint

def node_info():
    ec2 = boto3.client('ec2')
    response = ec2.describe_instances()
    pprint.pprint(response)

node_info()
