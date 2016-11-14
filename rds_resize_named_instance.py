# change instance_to_shrink to the name of the instance to resize
# and the sizes from and to.

instance_to_shrink='dbvault'
size_from='db.t2.micro'
size_to='db.t2.small'
 
import boto3

def lambda_handler(event, context):
 client=boto3.client('rds') 
 response=client.describe_db_instances()
 instances=response.get('DBInstances')

 for instance in instances:
   dbidentifier=instance.get('DBInstanceIdentifier')
   dbinstanceclass=instance.get('DBInstanceClass')
   status=instance.get('DBInstanceStatus')
  
   if dbidentifier == instance_to_shrink and status == 'available' and dbinstanceclass == size_from:
      print 'Server '+instance_to_shrink+' is available and ready to be resized'
      response=client.modify_db_instance(
         ApplyImmediately=True, 
         DBInstanceIdentifier=dbidentifier,
         DBInstanceClass=size_to
      )
