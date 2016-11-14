# change instance_to_shrink to the name of the instance to resize
# and the sizes from and to.

import boto3
 
def lambda_handler(event, context):
 client          = boto3.client('rds')
 
 instance_to_shrink='dbvault'
 response        = client.describe_db_instances()
 instances       = response.get('DBInstances')

 for instance in instances:
   dbidentifier = instance.get('DBInstanceIdentifier')
   dbinstanceclass = instance.get('DBInstanceClass')
   status = instance.get('DBInstanceStatus')
  
   if dbidentifier == instance_to_shrink and status == 'available' and dbinstanceclass == 'db.t2.small':
      print 'Server is available and ready to be downsized'
      response = client.modify_db_instance(ApplyImmediately=True, DBInstanceIdentifier=dbidentifier,DBInstanceClass='db.t2.micro')


