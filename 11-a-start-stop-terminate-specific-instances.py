# This script will start specific EC2 instances using client method to start instances.
# The script would wait until the instances reach running state.
# The script would collect specific instance details using collection concept.

# Import modules.

import boto3

# Initiate the AWS session using ec2-admin profile.

aws_session = boto3.session.Session(profile_name="inderpalaws02-ec2-admin")

# Initiate the EC2 resource for collection.

ec2_resource = aws_session.resource(service_name="ec2",region_name="us-east-1")

# Initiate the EC2 client to start specific instances.

ec2_client = aws_session.client(service_name="ec2",region_name="us-east-1")

# Collect the specific instance ids which need to be started.
# Here, we'll start only servers in DEV environment.
# The instances in DEV environment have a tag as Environment set to DEV.
# So, instance ids would be collected based on the tags value and collection concept.

ec2_collection = ec2_resource.instances     # Initiate the collection object.

# Collect the DEV environment's instances' id details.

filter1 = {"Name":"tag:Environment","Values":["DEV"]}   # Initiate the filter for Environment tag with value DEV.
ec2_iterator = ec2_collection.filter(Filters=[filter1])
instance_id_list = []       # Initiate the empty list to hold instance ids of instances with Environment tag set to DEV.
for instance in ec2_iterator:
    instance_id_list.append(instance.id)
#print(instance_id_list)

# Start the instances of DEV environment.

print(f"\nStarting the DEV environment's instances. This would take few minutes...")
response = ec2_client.start_instances(InstanceIds=instance_id_list)

# Initiate the waiter using the client.

ec2_waiter = ec2_client.get_waiter("instance_running")

# Initiate the wait until the DEV environment's instances reach running state.

ec2_waiter.wait(InstanceIds=instance_id_list)

# Display final message when instances reach running state.

print(f"\nThe instances in DEV environment are up and running now.")

# Here, we filtered the specific instances using filter on EC2 resource object (collection).
# In next script, we'll do same using filter on EC2 client object. So, it would be like doing everything using client.
