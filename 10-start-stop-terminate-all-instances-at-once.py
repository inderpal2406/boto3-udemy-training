# This script will start all instances using collection method and wait until all instances reach running state.

# Import modules.

import boto3

# Initiate AWS session using ec2-admin profile.

aws_session = boto3.session.Session(profile_name="inderpalaws02-ec2-admin")

# Initiate EC2 service resource for collection based operations.

ec2_resource = aws_session.resource(service_name="ec2",region_name="us-east-1")

# Initiate EC2 service client for waiter.

ec2_client = aws_session.client(service_name="ec2",region_name="us-east-1")

# Initiate the waiter using the client.

ec2_waiter = ec2_client.get_waiter("instance_running")

# Initiate EC2 collection object.

ec2_collection = ec2_resource.instances
# print(dir(ec2_collection))    # Will print available functions for the object.
# In these functions, we focussed on all(), limit(), filter() functions in previous script.
# Now, we'll focus on rest of the functions like reboot, start, stop, terminate, etc.

# Create the list of instance ids of all instances, inorder to pass the list to the waiter.

instance_id_list = []   # Initiate empty list.
ec2_iterator = ec2_collection.all()
for instance in ec2_iterator:
    #print(instance.id)
    instance_id_list.append(instance.id)
#print(instance_id_list)

# Start all the instances.

print(f"Starting all instances. This will take few minutes...")
response = ec2_collection.start()
# Initiate the wait until the instances are in running state.
ec2_waiter.wait(InstanceIds=instance_id_list)
print(f"All instances are up and running now.")

# In similar way, we can try other functions like reboot(), stop(), terminate().
# Above functions work on all instances and we cannot specify a specific subset of instance ids to be operated on, in above functions.
# To overcome this, we'll use client method to start specific instances in next script.
# To collect specific instances' details, we'll use collection.
