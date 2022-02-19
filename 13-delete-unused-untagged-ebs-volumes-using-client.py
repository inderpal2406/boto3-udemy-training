# This script will delete the volumes which are in available state and has no tags attached to it.
# Available state means that the volume is not attached to any instance.

# Import modules.

import boto3

# Create AWS session with ec2-admin profile.

aws_session = boto3.session.Session(profile_name="inderpalaws02-ec2-admin")

# Create EC2 service client.

ec2_client = aws_session.client(service_name="ec2",region_name="us-east-1")

# List and delete the unused and untagged volumes using client.

filter1 = {"Name":"status","Values":["available"]}  # Filter to list only available volumes. This filter is created after testing till line 26 (printing all volumes).
response = ec2_client.describe_volumes(Filters=[filter1])   # Filter only the available volumes from all volumes.
#print(response)
#print(response.keys())
#print(response["Volumes"])
for volume in response["Volumes"]:
    #print(volume,"\n")
    #print(volume.keys(),"\n")
    #print(volume["VolumeId"],volume["State"],volume["Tags"])   # This gives error for the untagged value, as it doesn't have "Tags" key in it's dict.
    #if "Tags" in volume.keys():     # Condition to list volume id which has "Tags" key.
    if "Tags" not in volume.keys():
        #print(volume["VolumeId"])
        #print(dir(volume))     # This lists methods & variables available for the dict. This doesn't list function to delete the volume.
        print(f"Deleting the unused and untagged volume: {volume['VolumeId']}")
        ec2_client.delete_volume(VolumeId=volume['VolumeId'])
        print(f"The volume is deleted now.")
