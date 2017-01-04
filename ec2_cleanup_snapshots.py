import json
import string
import datetime
import boto3

#put here the AWS account id
account_id='852857041816'

def lambda_handler(event, context):
    
    ec2 = boto3.client('ec2')
    snap_list = ec2.describe_snapshots().get('SnapshotId',[])
     
    # compute the cut-off time for snapshots
    cut_date=datetime.datetime.now()-datetime.timedelta(days=15)
        
    for dbsnaps in snap_list:
            inst_id=dbsnaps['SnapshotIdentifier']
            snap_date=datetime.datetime.strptime(str(dbsnaps['SnapshotCreateTime'])[:19], "%Y-%m-%d %H:%M:%S")
            
            if snap_date<cut_date:
                # check tags first 
                response = rdscon.list_tags_for_resource(
                    ResourceName='arn:aws:rds:eu-west-1:'+account_id+':snapshot:'+inst_id,
                    Filters=[]
                    )
                
                # requires the tags 'Purgeable'    
                for tag in response['TagList']:
                   if tag['Key'] == 'Purgeable' and tag['Value']=='True':
                     print "*** deleting arn:aws:rds:eu-west-1:"+account_id+":snapshot:" + inst_id    
                   else: 
                    print ">>> skipping arn:aws:rds:eu-west-1:"+account_id+":snapshot:"+inst_id 
                    
                    # rdscon.delete_db_snapshot(DBSnapshotIdentifier=inst_id)
