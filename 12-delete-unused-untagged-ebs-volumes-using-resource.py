# This script will delete the volumes which are in available state and has no tags attached to it.
# Available state means that the volume is not attached to any instance.

# Import modules.

import boto3

# Initiate AWS session with ec2-admin profile.

aws_session = boto3.session.Session(profile_name="inderpalaws02-ec2-admin")

# Create EC2 service resource.

ec2_resource = aws_session.resource(service_name="ec2",region_name="us-east-1")

# Create collection object.

ec2_collection = ec2_resource.volumes

# List all volumes which are in available state.

#volume_iterator = ec2_collection.all()  # Will pick up all volumes.
filter1 = {"Name":"status","Values":["available"]}  # Define filter to list only available volumes.
volume_iterator = ec2_collection.filter(Filters=[filter1])
for volume in volume_iterator:
    #print(volume)
    #print(volume.id)
    #print(dir(volume))
    #break
    #print(volume.id,volume.state,volume.tags)
    #if volume.tags:     # This condition will be True if the volume has tags.
    if not volume.tags:  # This condition will be True if the volume has no tags.
        #print(volume.id,volume.state,volume.tags)
        #print(dir(volume))
        print(f"Deleting the unused and untagged volume: {volume.id}")
        volume.delete()
        print(f"The volume is deleted now.")
