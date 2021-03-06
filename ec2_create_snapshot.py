import json
import boto3
import datetime
import time

account_id='852857041816'
volume_id='vol-1ea15bce'

def lambda_handler(event, context):
  client=boto3.client('ec2')
  response = client.create_snapshot(VolumeId=volume_id, Description='lambda-generated-snapshot')
  my_snap=response['SnapshotId']
  response=client.describe_snapshots(SnapshotIds=[ my_snap ])
  
  while response['Snapshots'][0]['State'] != 'completed':
      print ("Snapshot "+my_snap+" in progress... "+response['Snapshots'][0]['Progress'])
      time.sleep(20)
      response=client.describe_snapshots(SnapshotIds=[ my_snap ])
  
  # mark the snapshot "Purgeable" so it can be cleaned by the other script
  client.create_tags(Resources=[ my_snap ], Tags=[ { 'Key': 'Purgeable', 'Value': 'True' } ] ) 
  print ("Snapshot "+my_snap+" completed and tagged successfully")
  return (0)
