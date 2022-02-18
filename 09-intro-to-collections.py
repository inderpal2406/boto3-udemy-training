# Import modules.

import boto3

# Initiate AWS session with ec2-admin profile.

aws_session = boto3.session.Session(profile_name="inderpalaws02-ec2-admin")

# Initiate EC2 resource because collections exist for service resource.

ec2_resource = aws_session.resource(service_name="ec2",region_name="us-east-1")

# Initiate collection object.

ec2_collection = ec2_resource.instances
# print(dir(ec2_collection))    # Will print available functions for the object.
# In these functions, we'll focus on all(), limit(), filter() functions for now. Rest will be seen later.

# Print all instances using all() function. all() creates an iterable through which we'll iterate and print the instances.

print(f"\nAll ec2 instances are as below,")
ec2_iterator = ec2_collection.all()
for instance in ec2_iterator:
    print(instance)

# Print only first x ec2 instances. Here, x=1.

print(f"\nThe first ec2 instance in the list of all instances is as below,")
ec2_iterator = ec2_collection.limit(1)
for instance in ec2_iterator:
    print(instance)

# Print all instances using filter().

print(f"\nAll ec2 instances using filter(), are as below,")
ec2_iterator = ec2_collection.filter()
for instance in ec2_iterator:
    print(instance)

# Print only the running instances using filter().

print(f"\nThe ec2 instances which are in running state are as below,")
filter1 = {"Name":"instance-state-name","Values":["running"]}
ec2_iterator = ec2_collection.filter(Filters=[filter1])
for instance in ec2_iterator:
    print(instance)

# Print only the stopped instances using filter().

print(f"\nThe ec2 instances which are in stopped state are as below,")
filter1 = {"Name":"instance-state-name","Values":["stopped"]}
ec2_iterator = ec2_collection.filter(Filters=[filter1])
for instance in ec2_iterator:
    print(instance)

# Print the running and stopped instances using filter().

print(f"\nThe ec2 instances which are in running and stopped state are as below,")
filter1 = {"Name":"instance-state-name","Values":["running","stopped"]}
ec2_iterator = ec2_collection.filter(Filters=[filter1])
for instance in ec2_iterator:
    print(instance)

# Print the instances which are in stopped state and have instance type as t2.micro.

print(f"\nThe ec2 instances which are in stopped state and have instance type as t2.micro, are as below,")
filter1 = {"Name":"instance-state-name","Values":["stopped"]}
filter2 = {"Name":"instance-type","Values":["t2.micro"]}
ec2_iterator = ec2_collection.filter(Filters=[filter1,filter2])
for instance in ec2_iterator:
    print(instance)
