# This script will start a stopped EC2 instance.
# But will wait until the instance comes to running state. And then display the result.
# The logic to implement the wait of transition between the states is using Boto3 waiters here.

# Import modules.

import boto3

# Initiate the AWS session using ec2-admin profile.

aws_session = boto3.session.Session(profile_name="inderpalaws02-ec2-admin")

# Initiate the EC2 client.

ec2_client = aws_session.client(service_name="ec2",region_name="us-east-1")

# Display purpose of the script.

print(f"This script will accept an EC2 instance id from the user and would start it.")
print(f"Prompt would be returned once the EC2 instance reaches running state.\n")

# Accept the instance id from the user.

instance_id = input("Enter the EC2 instance id: ")

# Start the EC2 instance and wait until it reaches running state.

print(f"\nStarting the EC2 instance {instance_id}. This will take few minutes...")
start_response = ec2_client.start_instances(InstanceIds=[instance_id])
# Initiate the waiter using the client.
waiter = ec2_client.get_waiter("instance_running")
# Initiate the wait until instance reaches running state.
waiter.wait(InstanceIds=[instance_id])
print("\nInstance is now up and running.")

# Waiter using the client object would do 40 checks at interval of 15 seconds.
# Waiter using resource object would do 40 checks at interval of 5 seconds.
# In this script we have used the waiter using the client object.
# As per the instructor, in real world, it is better to use client object waiter as it offers more duration of check.
# We never know how much time would it take to bring up an instance.
