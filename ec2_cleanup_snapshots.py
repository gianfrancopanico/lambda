import json
import string
import datetime
import boto3

#put here the AWS account id
account_id='852857041816'

def lambda_handler(event, context):
    
    ec2 = boto3.client('ec2')
    snap_list = ec2.describe_snapshots()
    
    # compute the cut-off time for snapshots
    cut_date=datetime.datetime.now()-datetime.timedelta(days=15)
        
    for volsnaps in snap_list['Snapshots']:
        snap_date=datetime.datetime.strptime(str(volsnaps['StartTime'])[:19], "%Y-%m-%d %H:%M:%S")
        inst_id=volsnaps['SnapshotId']
        print inst_id+" "+str(snap_date)
           
    return (0)
