# This script will create inventory of all EC2 instances in us-east-1 region in form of a CSV file.

# Import modules.

import boto3
import csv

# Initiate AWS session with ec2-admin profile.

aws_session = boto3.session.Session(profile_name="inderpalaws02-ec2-admin")

# Initiate EC2 service client.

ec2_client = aws_session.client(service_name="ec2",region_name="us-east-1")

# List EC2 instance details and create a CSV file.

count = 1   # Initiate a counter for serial number.
#csv_ob = open("ec2-inventory.csv","w")  # Open CSV inventory file in write mode. This leaves one row between successive entries.
csv_ob = open("ec2-inventory.csv","w",newline='')
csv_wr = csv.writer(csv_ob)
csv_wr.writerow(["Sr.No.","InstanceId","InstanceType","LaunchTime","PrivateIpAddress"])
response = ec2_client.describe_instances()
#print(response)
#print(response["Reservations"])
for reservation in response["Reservations"]:
    #print(reservation)
    #print(reservation.keys())
    #print(reservation["Instances"])
    for instance in reservation["Instances"]:
        #print(instance)
        #print(instance.keys())
        #print(count,instance["InstanceId"])
        csv_wr.writerow([count,instance["InstanceId"],instance["InstanceType"],instance["LaunchTime"],instance["PrivateIpAddress"]])
    count = count + 1
csv_ob.close()
print(f"The inventory file ec2-inventory.csv is created in current directory.")
