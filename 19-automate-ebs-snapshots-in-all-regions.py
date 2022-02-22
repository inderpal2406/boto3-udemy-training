# This script will take snapshots of EBS volumes attached to EC2 instances with tag Environment:PROD, in all enabled regions for our account.

# Import modules.

from tracemalloc import Snapshot
import boto3

# Get list of enabled regions for our account.

aws_session = boto3.session.Session(profile_name="inderpalaws02-aws-admin")

ec2_client = aws_session.client(service_name="ec2")

region_name_list = []

response = ec2_client.describe_regions()

for region in response["Regions"]:
    #print(region["RegionName"])
    region_name_list.append(region["RegionName"])

#print(region_name_list)

# Loop through each region in region_name_list to create a client, then create a list of PROD 
# volumes in that region, then loop through the list of volumes to create corresponding snapshots.

for region in region_name_list:
    ec2_client = aws_session.client(service_name="ec2",region_name=region)
    volume_id_list = []
    filter1 = {"Name":"tag:Environment","Values":["PROD"]}
    response = ec2_client.describe_volumes(Filters=[filter1])
    for volume in response["Volumes"]:
        for attachment in volume["Attachments"]:
            volume_id_list.append(attachment["VolumeId"])
    if len(volume_id_list) == 0:
        print(f"No EBS volumes found in {region} AWS region. Proceeding to next region.")
        continue
    snapshot_id_list = []
    print(f"Starting to take snapshots in {region} AWS region.")
    for volume_id in volume_id_list:
        response = ec2_client.create_snapshot(VolumeId=volume_id,
        TagSpecifications = [
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
        snapshot_id_list.append(response["SnapshotId"])
    waiter = ec2_client.get_waiter("snapshot_completed")
    waiter.wait(SnapshotIds=snapshot_id_list)
    print(f"Snaphots completed for PROD EBS volumes in {region} AWS region.")

# Same script can be used as a lambda function by using default session. 
# This lambda function would need an IAM role to have full access to EC2 service.
# Waiters can be excluded in Lambda to reduce execution time.
# Also, timeout needs to be setup as per the time needed to start snapshots of all PROD volumes 
# in all regions. This depends on number of volumes being operated on.
