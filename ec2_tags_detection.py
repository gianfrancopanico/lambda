from __future__ import print_function

import json
import boto3
import botocore

aws_tags=['Name','Description','email','owner','environment','costcentre','project']
ADMIN_EMAIL="aws.admin@sainsburys.co.uk"
ToAddresses="aws.admin@sainsburys.co.uk"

print('Loading function')


def lambda_send_email():
     client_email = boto3.client('ses')

     response = client_email.send_email(
        Source=ADMIN_EMAIL,
        Destination={
            'ToAddresses':  [
            	ToAddresses
            ]
        },
        Message={
            'Subject': {
            'Data': subject
        },
        'Body': {
            'Html': {
                'Data': message
            }
           }
        }
    )


def lambda_handler(event, context):
    global subject
    global message
    ec2_client = boto3.client("ec2")
    ec2 = boto3.resource('ec2')

    #print ("Received event: " + json.dumps(event, indent=2))
    #print ("************************************************")


    print ("Event Region :" + event['region'])
    print ("Event account :" + event['account'])
    event_time = event['detail']['eventTime']
    print ("Event Time :" + event_time)

    try:
        resource_name=[key['resourceId'] for key in event['detail']['requestParameters']['resourcesSet']['items']]
        resource_id=str(resource_name[0])
        print ("resource_id: " + str(resource_id))
    except botocore.exceptions.ClientError as e:
        #if e.response['Erroddr']['Code'] == 'EntityAlreadyExists':
            #print "Resource already exists"
        #else:
            print ("Unexpected error: %s" % e)
            return false

    instance_id = ec2.Instance(resource_id)

    subject="Tagging Detection System, Instance: " + str(resource_name) + " From Account: " + event['account'] + " And Region: " + event['region']

    if instance_id.tags is None:
        message="Instance: %s  Does NOT have Tags\n********"  % (instance_id)
        lambda_send_email()

    tag_missing=[]
    for tag in aws_tags:
        tags_existing=[]
        for instance_tag in instance_id.tags:
            tag_key = instance_tag.get('Key')
            tags_existing.append(tag_key)

        if tag not in tags_existing:
            tag_missing.append(tag)
            #print ("tag_missing:" + str(tag_missing))

    if tag_missing:
        print (tag_missing)
        body1="Got Missing Tags or the wrong tagging name.\nMissing tags:" + str(tag_missing) + "\nCurrent Tags:" + str(tags_existing)
	body2="Read the Following RFC for further Details\n https://github.com/JSainsburyPLC/ops-architecture/blob/master/RFCs/RFC002-AWS-tagging-policy.md"
	message=body1 + body2
        #print ("ADMIN_EMAIL: " + ADMIN_EMAIL + "\nToAddresses: " + ToAddresses + "\nsubject: " + subject + "\nmessage: " + message)
        print (message)

        lambda_send_email()
