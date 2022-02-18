# This script will stop specific EC2 instances using client method to stop instances.
# The instances started in previous script would be stopped in this script.
# The script would wait until the instances reach stopped state.
# The script would collect specific instance details using client method as compared to collection concept in previous script.

# Import modules.

import boto3

# Initiate AWS session with ec2-admin profile.

aws_session = boto3.session.Session(profile_name="inderpalaws02-ec2-admin")

# Initiate EC2 client.

ec2_client = aws_session.client(service_name="ec2",region_name="us-east-1")

# Collect the specific instance ids which need to be stopped.
# Here, we'll stop only servers in DEV environment.
# The instances in DEV environment have a tag as "Environment" set to "DEV".
# So, instance ids would be collected based on the tags value and client method.

filter1 = {"Name":"tag:Environment","Values":["DEV"]}   # Initiate the filter based on tag value.
instance_id_list = []   # Initiate the empty list to hold instance ids.
response = ec2_client.describe_instances(Filters=[filter1]) # Get instance details based on filter.
# Refine the response to pick up only the instance ids.
# print(response)
# print(response["Reservations"])
for reservation in response["Reservations"]:
    #print(reservation)
    #print(reservation["Instances"])
    for instance in reservation["Instances"]:
        #print(instance)
        #print(instance["InstanceId"])
        instance_id_list.append(instance["InstanceId"])
#print(instance_id_list)     # List of required instance ids has got generated.

# Stop the instances.

print(f"\nStopping the DEV environment's instances. This would take few minutes...")
response = ec2_client.stop_instances(InstanceIds=instance_id_list)

# Initiate the waiter.

ec2_waiter = ec2_client.get_waiter("instance_stopped")

# Initiate the wait until the instances reach stopped state.

ec2_waiter.wait(InstanceIds=instance_id_list)

# Display final message.

print(f"\nThe instances are stopped now.")
