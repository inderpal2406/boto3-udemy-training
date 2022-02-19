# This script will list snapshot ids of all snapshots owned by me (current AWS account).

# Import modules.

import boto3

# Initiate AWS session with ec2-admin profile.

aws_session = boto3.session.Session(profile_name="inderpalaws02-ec2-admin")

# Initiate EC2 service client.

ec2_client = aws_session.client(service_name="ec2",region_name="us-east-1")

# List all snapshot ids.

#response = ec2_client.describe_snapshots()
#print(response)     # This prints a lot of data. Public, private, owned by me, snapshots are listed.

# Hence, we'll now try to print the snapshots owned by our AWS account only.
# Get the AWS account id.

sts_client = aws_session.client(service_name="sts",region_name="us-east-1")     # Initiate STS service client.
#print("The AWS account id is: ",sts_client.get_caller_identity().get("Account"))
aws_account_id = sts_client.get_caller_identity().get("Account")

print(f"The snapshots owned by the AWS account {aws_account_id} are as below,\n")
response = ec2_client.describe_snapshots(OwnerIds=[aws_account_id])
#print(response)     # We get a dictionary.
#print(response.keys())
#print(response["Snapshots"])    # Print the Snapshots key values. We get a list.
for snapshot in response["Snapshots"]:      # Iterate over each value of the list.
    #print(snapshot,"\n")    # We get each value in list as a dict.
    #print(snapshot.keys(),"\n")
    print(snapshot["SnapshotId"])
print() # Leave a line.
