# This script will take snapshots of EBS volumes attached to EC2 instances with tag Environment:PROD.

# General notes:
# 1. Ensure the EC2 instance whose EBS volumes need to be backed up, that EC2 instance's EBS
#    volumes have correct tags. The volumes would be picked up based on tags.
# 2. The EBS volumes attached to an EC2 instance automatically gets the tags of the EC2 instance.

# Import modules.

import boto3

aws_session = boto3.session.Session(profile_name="inderpalaws02-ec2-admin")

ec2_client = aws_session.client(service_name="ec2",region_name="us-east-1")

volume_id_list = []

filter1 = {"Name":"tag:Environment","Values":["PROD"]}

response = ec2_client.describe_volumes(Filters=[filter1])

for volume in response["Volumes"]:
    for attachment in volume["Attachments"]:
        volume_id_list.append(attachment["VolumeId"])

snapshot_id_list = []

print(f"Starting to take snapshots. This will take few minutes...\n")
for volume_id in volume_id_list:
    print(f"Starting snapshot of volume: {volume_id}")
    response = ec2_client.create_snapshot(VolumeId=volume_id,
    TagSpecifications= [
        {
            "ResourceType": "snapshot",
            "Tags": [
                {
                    "Key":"DeleteAfter",
                    "Value":"90"
                }
            ]
        }
    ]
    )
    # Having a waiter in each iteration woulld take longer as next snapshot will be initiated only if previous one completed.
    # So, we'll create a list of all snapshot ids which will be passed to waiter outside the loop.
    #waiter = ec2_client.get_waiter("snapshot_completed")
    #waiter.wait(SnapshotIds=[response["SnapshotId"]])
    #print(f"Snapshot {response['SnapshotId']} completed.")
    snapshot_id_list.append(response["SnapshotId"])     # Waiter needs to be provided snapshot id which is picked up from response here.

waiter = ec2_client.get_waiter("snapshot_completed")
waiter.wait(SnapshotIds=snapshot_id_list)
print(f"\nSnapshots of all production EBS volumes is completed.")

# This script would be used as a lamda function with few modifications, to take snapshots of prod volumes once a day.
