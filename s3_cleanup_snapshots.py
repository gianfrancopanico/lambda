import json
import string
import datetime
import boto3

#put here the AWS account id
account_id='108652351904'

def lambda_handler(event, context):
    
    rdscon = boto3.client('rds')
    rdb = rdscon.describe_db_snapshots().get(
        'DBSnapshots',[] 
        )
    
    # compute the cut-off time for snapshots
    cut_date=datetime.datetime.now()-datetime.timedelta(days=15)
        
    for dbsnaps in rdb:
            inst_id=dbsnaps['DBSnapshotIdentifier']
            snap_date=datetime.datetime.strptime(str(dbsnaps['SnapshotCreateTime'])[:19], "%Y-%m-%d %H:%M:%S")
            
            if snap_date<cut_date:
                # check tags first 
                response = rdscon.list_tags_for_resource(
                    ResourceName='arn:aws:rds:eu-west-1:'+account_id+':snapshot:'+inst_id,
                    Filters=[]
                    )
                
                # requires the tags 'write-protected' and 'email' to be present    
                mvp=0     
                for tag in response['TagList']:
                   if tag['Key'] == 'write-protected' and tag['Value']=='true':
                       mvp=mvp+1
                   if tag['Key'] == 'email': 
                       mvp=mvp+1
                
                # if both tags are present, skip
                if (mvp >= 2):
                    print ">>> skipping arn:aws:rds:eu-west-1:"+account_id+":snapshot:"+inst_id 
                else: 
                    # otherwise exterminate
                    print "*** deleting arn:aws:rds:eu-west-1:"+account_id+":snapshot:" + inst_id 
                    rdscon.delete_db_snapshot(DBSnapshotIdentifier=inst_id)
