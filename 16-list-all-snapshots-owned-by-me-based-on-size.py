# This script will list snapshot ids of all snapshots owned by me (current AWS account) based on specified size.

# Import modules.

from tracemalloc import Snapshot
import boto3

# Initiate AWS session with ec2-admin profile.

aws_session = boto3.session.Session(profile_name="inderpalaws02-ec2-admin")

# Initiate EC2 service client.

ec2_client = aws_session.client(service_name="ec2",region_name="us-east-1")

# Get AWS account ID.

sts_client = aws_session.client(service_name="sts",region_name="us-east-1")     # Initiate STS service client.
aws_account_id = sts_client.get_caller_identity()["Account"]
#print(aws_account_id)

# List snapshots owned by AWS account based on a specific size.

filter1 = {"Name":"volume-size","Values":["8"]}   # Filter to get snapshots of size 8 GB. Filter created after coding till line 33.
# IMP Note: The value key in filter accepts only string as per official documentation. If we provide an int, then it fails.
response = ec2_client.describe_snapshots(OwnerIds=[aws_account_id],Filters=[filter1])
#print(response)
#print(response.keys())
#print(response["Snapshots"])
for snapshot in response["Snapshots"]:
    #print(snapshot)
    #print(snapshot.keys())
    #print(snapshot["SnapshotId"],snapshot["VolumeSize"])
    print(snapshot["SnapshotId"])
