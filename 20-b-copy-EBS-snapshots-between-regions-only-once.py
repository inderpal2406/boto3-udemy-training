# This script is an enhancement to previous script 20-a.
# In previous script, if we trigger the script multiple times, then that many times, the 
# snapshots would get copied to other region.
# This will result in multiple backup/disaster recovery copies of same snapshot in destination 
# region.
# But we need it in such a way that if the snapshot is copied from source region to destination 
# region for once, then its backup/disaster recovery copy is created. After this even if run the 
# script multiple times, it should not copy the snapshot from source to destination region.
# So, this script is developed to achieve this functionality.

# Import modules.

import boto3

# Create AWS session with EC2 admin profile.

aws_session = boto3.session.Session(profile_name="inderpalaws02-ec2-admin")

# Create STS Client to get AWS account ID to fetch only the snapshots owned by the account.

sts_client = aws_session.client(service_name="sts",region_name="us-east-1")

response = sts_client.get_caller_identity()
aws_account_id = response["Account"]

# So, the AWS account ID gets fetched with EC2 admin profile and us-east-1 region.

# Define variables.

source_region = "us-east-1"
dest_region = "us-west-1"

# Initiate EC2 client to fetch snapshot ids from source region.

source_ec2_client = aws_session.client(service_name="ec2",region_name=source_region)

# Create empty list to hold snapshot ids from source region.

source_snapshot_id_list = []

# Describe filter to fetch snapshot ids of snapshots having tag:DisasterRecovery set to "Yes"

filter1 = {"Name":"tag:DisasterRecovery","Values":["Yes"]}

response = source_ec2_client.describe_snapshots(OwnerIds=[aws_account_id],Filters=[filter1])

for snapshot in response["Snapshots"]:
    source_snapshot_id_list.append(snapshot["SnapshotId"])

# Test is the list of snapshot ids from source region with required tag is empty.
# If empty, then it means there is not snapshot to be copied to destination region.
# Hence, exit the script.

if bool(source_snapshot_id_list) is False:
    print(f"No snapshot found in {source_region} with required tag to be copied to {dest_region}.")
    print(f"Hence, exiting script without any action.")
    exit()

# Create empty list to hold snapshot ids created after copy takes place.
# This list is needed to pass to the waiter to wait till the snapshots are completed.

dest_snapshot_id_list = []

# Define EC2 client to create snapshots in destination region.

dest_ec2_client = aws_session.client(service_name="ec2",region_name=dest_region)

# Copy the snapshot from source region to destination region one by one.

for snap_id in source_snapshot_id_list:
    print(f"Copying snapshot {snap_id} from {source_region} to {dest_region}.")
    response = dest_ec2_client.copy_snapshot(
        SourceRegion=source_region,
        SourceSnapshotId=snap_id,
        TagSpecifications=[
            {
                "ResourceType": "snapshot",
                "Tags": [
                    {
                        "Key": "DeleteAfter",
                        "Value": "90"
                    },
                ]
            },
        ]
    )
    dest_snapshot_id_list.append(response["SnapshotId"])
    # Change tag value after copy to prevent multiple copies of same snapshot due to multiple runs of the script.
    # This tag:DisasterRecovery will be changed from "Yes" to "Completed" for snapshot in source region.
    # The tag with old value will be deleted, and then created again with new value.
    source_ec2_client.delete_tags(Resources=[snap_id],Tags=[{"Key":"DisasterRecovery","Value":"Yes"}])
    source_ec2_client.create_tags(Resources=[snap_id],Tags=[{"Key":"DisasterRecovery","Value":"Completed"}])
    # Now in next run of the script, same snapshot won't get copied again to dest region as the tag has got changed now.

# Display message to wait until snapshot copy completes in destination region.

print(f"Snapshot copy to {dest_region} destination AWS region would take some time. Please wait...")

# Initiate waiter to wait until snapshot copy/creation in destination region completes.

waiter = dest_ec2_client.get_waiter("snapshot_completed")

# Initiate the wait for the snapshot ids in destination region.

waiter.wait(SnapshotIds=dest_snapshot_id_list)

# Print final message of completion after wait is over.

print(f"Snapshot copy to {dest_region} destination AWS region is completed.")

# This script can be scheduled in lambda as well with proper role/permissions and trigger.
