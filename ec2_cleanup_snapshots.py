import json
import string
import datetime
import boto3

#put here the AWS account id
account_id='852857041816'
num_days=15

# compute the cut-off time for snapshots
cut_date=datetime.datetime.now()-datetime.timedelta(days=num_days)

def lambda_handler(event, context):
    
    ec2 = boto3.client('ec2')
    
    # select from volume_snapshots where purgeable=true
    purgeable = ec2.describe_tags(Filters=[{ 'Name': 'tag:Purgeable', 'Values': [ 'True' ] }])
    
    for volsnap in purgeable['Tags']: 
        snap_info=ec2.describe_snapshots(SnapshotIds=[ volsnap['ResourceId'] ]) 
        snap_date=datetime.datetime.strptime(str(snap_info['Snapshots'][0]['StartTime'])[:19], "%Y-%m-%d %H:%M:%S")
        print volsnap['ResourceId']+" "+str(snap_date)+" "+str(cut_date)
           
    return (0)
