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
        
    #rdblist = len(rdb)
    #print "Found ", rdblist, " snapshots"    
    
    # compute the cut-off time for snapshots (set days here!) 
    cut_date=datetime.datetime.now()-datetime.timedelta(days=15)
        
    for dbsnaps in rdb:
            inst_id=dbsnaps['DBSnapshotIdentifier']
            snap_date=datetime.datetime.strptime(str(dbsnaps['SnapshotCreateTime'])[:19], "%Y-%m-%d %H:%M:%S")
            
            if snap_date<cut_date:
                # exterminate
                print "*** " + inst_id + " marked for deletion [" + str(snap_date)[:10] + " < " + str(cut_date)[:10] + "]"
                rdscon.delete_db_snapshot(
                    DBSnapshotIdentifier=inst_id
                )
