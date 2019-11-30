import boto3
import sys
import os
import traceback

nodes_remove = []
maxLengthList = 6


try:
    while len(nodes_remove) < maxLengthList:
        user = input('Enter host id: ')
        nodes_remove.append(user)
        if user=='':
            for nodes in nodes_remove:
                ids = [nodes]
                ec2 = boto3.resource('ec2')
                ec2.instances.filter(InstanceIds = ids).terminate()
except:
        errorFile = open('aws_log.txt','w')
        errorFile.write(traceback.format_exc())
        errorFile.close()
