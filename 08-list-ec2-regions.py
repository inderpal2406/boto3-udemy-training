# This script will print the available AWS regions for EC2 service in the AWS account.

# Import modules.

import boto3

# Initiate AWS session using ec2-admin profile.

aws_session = boto3.session.Session(profile_name="inderpalaws02-ec2-admin")

# Initiate the EC2 client.

ec2_client = aws_session.client(service_name="ec2",region_name="us-east-1")

# Get the region names which are enabled for our account.

print(f"The regions enabled for your account are as below,\n")
count = 0
response = ec2_client.describe_regions()
#print(response["Regions"])
for region in response["Regions"]:
    print(region["RegionName"])
    count = count + 1
print(f"\nThe total number of regions enabled for your account is: {count}\n")
