import json
import boto3
import datetime
import time

account_id='852857041816'
region_id='us-east-1'
volume_id='vol-1ea15bce'

def lambda_handler(event, context):

  client=boto3.client('ec2')
  arn_id='arn:aws:ec2:'+region_id+':'+account_id+':volume/'+volume_id
  
  response = client.create_snapshot(
    VolumeId=volume_id,
    Description='lambda-generated-snapshot'
    )
  
