# lambda script to snapshot a named RDS instance

instance_to_backup='production-db'

import time
import datetime
import boto3
import json

def lambda_handler(event, context):
 client=boto3.client('rds') 
 response=client.describe_db_instances()
 instances=response.get('DBInstances')

 for instance in instances:
   dbidentifier=instance.get('DBInstanceIdentifier')
   status=instance.get('DBInstanceStatus')
   snap_id=(instance_to_backup + "-" + datetime.datetime.now().strftime("%Y%m%d-%H%M") ) 

   if dbidentifier == instance_to_backup and status == 'available':
      print 'Server '+instance_to_backup+' is available and ready to be snapshotted'

      snapped=client.create_db_snapshot(DBSnapshotIdentifier=snap_id,DBInstanceIdentifier=instance_to_backup)
      snap_status=client.describe_db_snapshots(DBSnapshotIdentifier=snap_id)
      while snap_status['DBSnapshots'][0]['Status'] != 'available':
          print("Snapshot in progress...")
          time.sleep(15)
          snap_status=client.describe_db_snapshots(DBSnapshotIdentifier=snap_id)
      print str(snap_status)
