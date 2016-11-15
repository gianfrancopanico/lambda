import json
import boto3

def lambda_handler(event, context):
 
    ec2 = boto3.resource('ec2')
    
    filters = [
        {
            'Name': 'instance-state-name', 
            'Values': ['running']
        }
    ]
    
    running_instances = ec2.instances.filter(Filters=filters)
 
    for instance in running_instances: 
        for tag in instance.tags:
            print str(tag)
            if tag['Key'] == 'write-protected':
              break
            else:
              ids=[ instance.id ]
              # postmortem=running_instances.filter(InstanceIds=ids).stop();
              print instance.id +" will be killed";
