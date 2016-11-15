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
    
    # looks for instances tagged as 'scale-down'
    for instance in running_instances: 
        for tag in instance.tags:
            if tag['Key'] == 'scale-down':
                print "*** "+instance.id+" is going to be scaled down..."  
                # stop the instance before resizing
                ec2.stop_instances(InstanceIds=[instance.id])
                waiter=ec2.get_waiter('instance_stopped')
                waiter.wait(InstanceIds=[instance.id])
                # Change the instance type
                ec2.modify_instance_attribute(InstanceId=instance.id, Attribute='instanceType', Value='m3.xlarge')           
                # Start the instance
                ec2.start_instances(InstanceIds=[instance.id])
