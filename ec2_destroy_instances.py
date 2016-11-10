import json
import boto3

def lambda_handler(event, context):
    # Check out the code below whenever you need to analyse the json output from the event.
    #print ("Received event: " + json.dumps(event, indent=2))
    #print ("************************************************")
    
    ec2 = boto3.resource('ec2')
    
    
    print "Event Region :", event['region']
    
    event_time = event['time']
    print "Event Time :", event_time
    
    time = event_time.split('T')
    t = time[1]
    t = t.split(':')
    hour = t[0]
    
    filters = [
        {
            'Name': 'instance-state-name', 
            'Values': ['running']
        }
    ]
    
    instances = ec2.instances.filter(Filters=filters)
    
    RunningInstances = [instance.id for instance in instances]
    
    if int(hour) > 19:
        print ("Right hour: " + int(hour))
        
    
    
    if len(RunningInstances) > 0 and int(hour) > 19:
            shuttingDown = ec2.instances.filter(InstanceIds=RunningInstances).stop()
            print shuttingDown
