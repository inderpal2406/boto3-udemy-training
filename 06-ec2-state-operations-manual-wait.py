# This script will start a stopped EC2 instance.
# But will wait until the instance comes to running state. And then display the result.

# Import modules.

import boto3
import time

# Initiate AWS session with ec2-admin profile.

aws_session = boto3.session.Session(profile_name="inderpalaws02-ec2-admin")

# Initiate EC2 service client.

ec2_client = aws_session.client(service_name="ec2",region_name="us-east-1")

# Display purpose of the script.

print(f"This script will accept an EC2 instance id from the user and would start it.")
print(f"Prompt would be returned once the EC2 instance reaches running state.\n")

# Accept the instance id from the user.

instance_id = input("Enter the EC2 instance id: ")

# Start the EC2 instance and wait until it reaches running state.

print(f"\nStarting the EC2 instance {instance_id}. This will take few minutes...")
start_response = ec2_client.start_instances(InstanceIds=[instance_id])
instance_state = "stopped"
while instance_state != "running":
    state_response = ec2_client.describe_instances(InstanceIds=[instance_id])
    #print(state_response["Reservations"])
    for each_reservation in state_response["Reservations"]:
        #print(each_reservation["Instances"])
        for each_instance in each_reservation["Instances"]:
            instance_state = each_instance["State"]["Name"]
            #print(instance_state)
    time.sleep(5)   # Introduce a delay to avoid frequent checks.
print("\nInstance started successfully.")
