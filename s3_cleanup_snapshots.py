import json
import string
import datetime
import boto3

def lambda_handler(event, context):
    print ("Starting with RDS snapshots")
    
    rdscon = boto3.client('rds')
    rdb = rdscon.describe_db_snapshots().get(
        'DBSnapshots',[] 
        )
        
    rdblist = len(rdb)
    print "Found ", rdblist, " snapshots"    
    cut_date=datetime.datetime.now()-datetime.timedelta(days=15)
        
    for dbsnaps in rdb:
            inst_id=dbsnaps['DBSnapshotIdentifier']
            inst_timestamp=dbsnaps['SnapshotCreateTime']
            snap_date=datetime.datetime.strptime(str(inst_timestamp), "20%y-%m-%d %h:%m:%s.%c+")
            # if inst_timestamp<cut_date: 
            #    print "***" 
            print inst_id, snap_date, cut_date
        
