# This script will first identify the snapshot ids that needs to be copied to other region.
# Such snapshots have a tag named DisasterRecovery set to Yes.
# Based on tag, the snapshot ids would be picked up.
# The copy is being done for Disaster Recovery purpose. 
# Copy would take place from us-east-1 to us-east-2 region.

# Import modules.

import boto3

# Define variables.

source_region = "us-east-1"
dest_region = "us-west-1"

aws_session = boto3.session.Session(profile_name="inderpalaws02-ec2-admin")

sts_client = aws_session.client(service_name="sts",region_name="us-east-1")

response = sts_client.get_caller_identity()

aws_account_id = response["Account"]

source_snapshot_id_list = []

# Define EC2 client for source region.

ec2_client = aws_session.client(service_name="ec2",region_name=source_region)

filter1 = {"Name":"tag:DisasterRecovery","Values":["Yes"]}

response  = ec2_client.describe_snapshots(OwnerIds=[aws_account_id],Filters=[filter1])

for snapshot in response["Snapshots"]:
    source_snapshot_id_list.append(snapshot["SnapshotId"])

dest_snapshot_id_list = []

# Define EC2 client for destination region.

ec2_client = aws_session.client(service_name="ec2",region_name=dest_region)

for snap_id in source_snapshot_id_list:
    print(f"Copying snapshot {snap_id} from {source_region} to {dest_region} AWS region.")
    response = ec2_client.copy_snapshot(SourceRegion=source_region,SourceSnapshotId=snap_id,
        TagSpecifications=[
            {
                "ResourceType": "snapshot",
                "Tags": [
                    {
                        "Key": "DeleteAfter",
                        "Value": "90"
                    }
                ]
            }
        ])
    dest_snapshot_id_list.append(response["SnapshotId"])

print(f"This may take few minutes to complete...")
waiter = ec2_client.get_waiter("snapshot_completed")
waiter.wait(SnapshotIds=dest_snapshot_id_list)
print(f"The snapshot copy is completed for all required snapshots.")
