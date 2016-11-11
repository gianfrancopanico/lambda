import json
import datetime
import boto3

def lambda_handler(event, context):
    # Check out the code below whenever you need to analyse the json output from the event.
    # print ("Received event: " + json.dumps(event, indent=2))
    
    rdscon = boto3.client('rds')
    
    # list any rds instances running 
    rdb = rdscon.describe_db_instances().get(
        'DBInstances',[] 
        )
        
    for dbinstance in rdb:
            inst_id=dbinstance['DBInstanceIdentifier'] 
            snap_id=( inst_id + "-" + datetime.datetime.now().strftime("%Y%m%d-%H%M") ) 
            print "Processing instance: ", inst_id
            print ">>> creating snapshot ", snap_id
            rdscon.delete_db_instance(
                DBInstanceIdentifier=inst_id, 
                FinalDBSnapshotIdentifier=snap_id,
                SkipFinalSnapshot=False
                )
            #create tags to make the actual snapshot undeleteable by other scripts
            rdscon.add_tags_to_resource(
                ResourceName='arn:aws:rds:eu-west-1:108652351904:snapshot:'+snap_id,
                Tags=[
                        {
                            'Key': 'Write-Protected', 
                            'Value': 'True'
                        },
                        {
                            'Key': 'Contact',
                            'Value': 'infradev-leads@sainsburys.co.uk'
                        }
                     ]
                )
            print ">>> terminating "
