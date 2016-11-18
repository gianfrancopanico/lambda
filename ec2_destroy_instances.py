import json
import boto3

def lambda_handler(event, context):
    ec2 = boto3.resource('ec2')
    
    # select the running instances only
    filters = [
        {
            'Name': 'instance-state-name', 
            'Values': ['running']
        }
    ]
    
    running_instances = ec2.instances.filter(Filters=filters)
    
    # stops all instances not tagged 'write-protected'
    for instance in running_instances: 
        kill_me=1
        for tag in instance.tags:
            if tag['Key'] == 'write-protected':
                print "*** "+instance.id+" is write protected..."
                kill_me=0
                break        
        if kill_me == 1:
            print instance.id +" will be killed";
            ids=[ instance.id ]
            postmortem=running_instances.filter(InstanceIds=ids).stop();
