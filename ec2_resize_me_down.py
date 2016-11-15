import boto3

client = boto3.client('ec2')

# Insert your Instance ID here
my_instance = 'i-7e261640'

# Stop the instance
client.stop_instances(InstanceIds=[my_instance])
waiter=client.get_waiter('instance_stopped')
waiter.wait(InstanceIds=[my_instance])

# Change the instance type
client.modify_instance_attribute(InstanceId=my_instance, Attribute='instanceType', Value='m3.xlarge')

# Start the instance
client.start_instances(InstanceIds=[my_instance])
