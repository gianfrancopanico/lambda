import json
import datetime
import boto3

def lambda_handler(event, context):
    # print ("Received event: " + json.dumps(event, indent=2))
    # print ("************************************************")
    
    rdscon = boto3.client('rds')
    rdb = rdscon.describe_db_instances().get(
        'DBInstances',[] 
        )
        
    # rdblist = len(rdb)
    # print "Found ", rdblist, " running servers"    
        
    for dbinstance in rdb:
            inst_id=dbinstance['DBInstanceIdentifier']
            snap_id=( inst_id + "-20" + datetime.datetime.now().strftime("%y%m%d-%H%M") ) 
            print "Processing instance: ", inst_id
            print ">>> creating snapshot ", snap_id
            
            rdscon.delete_db_instance(
                DBInstanceIdentifier=inst_id, 
                FinalDBSnapshotIdentifier=snap_id,
                SkipFinalSnapshot=False
                )
   
