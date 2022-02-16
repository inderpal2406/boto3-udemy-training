# This script will list the EC2 instance id, image id, instance type, state and time of last launch(start time).
# Also this script will list the EBS volume details in us-east-1 region.
# The EC2 details and EBS volume details are pulled using same EC2 client. 
# This is because, functions for both are available in EC2 client.
# We can relate this to EC2 console in AWS web GUI, in which on L.H.S., we have EBS, Images, Network & Security, load balancing, auto scaling sections.
# So, we can perform all L.H.S. section operations using EC2 client.

# Import modules.

import boto3

# Initiate AWS session with ec2-admin user.

aws_session = boto3.session.Session(profile_name="inderpalaws02-ec2-admin")

# Initiate EC2 service client.

ec2_client = aws_session.client(service_name="ec2",region_name="us-east-1")

# Display the EC2 instance details.

print(f"The EC2 instance details are as below,\n")
ec2_response = ec2_client.describe_instances()
for each_response in ec2_response["Reservations"]:
    #print(each_response["Instances"])
    for each_instance in each_response["Instances"]:
        #print(each_instance)
        print("Instance id: ",each_instance["InstanceId"])
        print("Image id: ",each_instance["ImageId"])
        print("Instance type: ",each_instance["InstanceType"])
        print("Instance state: ",each_instance["State"]["Name"])
        print("Instance launch time: ",each_instance["LaunchTime"])
    print()     # Leave a line.

# Describe EBS volume details.

print(f"The EBS volume details are as below,\n")
ebs_response = ec2_client.describe_volumes()
#print(response["Volumes"])
for each_response in ebs_response["Volumes"]:
    print("Volume Id: ",each_response["VolumeId"])
    #print(each_response["Attachments"])
    for each_attachment in each_response["Attachments"]:
        print("Volume attached to instance: ",each_attachment["InstanceId"])
        print("Volume attached as device: ",each_attachment["Device"])
        print("Volume state: ",each_attachment["State"])
    print("Volume availability zone: ",each_response["AvailabilityZone"])
    print("Volume Encryption: ",each_response["Encrypted"])
    print("Volume Size: ",each_response["Size"]," GB")
    print("Volume state: ",each_response["State"])
    print("Volume type: ",each_response["VolumeType"])
    print()     # Leave a line.
