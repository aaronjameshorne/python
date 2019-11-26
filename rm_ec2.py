import boto3
import sys
import os


def rm_ec2():
    nodes_remove = []
    maxLengthList = 6
    while len(nodes_remove) < maxLengthList:
        user = input('Enter host id: ')
        nodes_remove.append(user)
        if user=='':
            for nodes in nodes_remove:
                ids = [nodes]
                ec2 = boto3.resource('ec2')
                ec2.instances.filter(InstanceIds = ids).terminate()
                exit

rm_ec2()
