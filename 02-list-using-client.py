# Import modules.

import boto3

# Open AWS console sessions with different profiles.

iam_aws_console = boto3.session.Session(profile_name="inderpalaws02-iam-admin")
ec2_aws_console = boto3.session.Session(profile_name="inderpalaws02-ec2-admin")
s3_aws_console = boto3.session.Session(profile_name="inderpalaws02-s3-admin")

# Open AWS service consoles.

iam_aws_service = iam_aws_console.client(service_name="iam")
ec2_aws_service = ec2_aws_console.client(service_name="ec2",region_name="us-east-1")
s3_aws_service = s3_aws_console.client(service_name="s3",region_name="us-east-1")

# List all IAM users using client object.

print(f"The IAM users in the account are as below:")
for each in iam_aws_service.list_users()["Users"]:
    print(each["UserName"])

# List all EC2 instances in us-east-1 region.

print(f"The EC2 instances in the us-east-1 region are as below:")
for each_reservation in ec2_aws_service.describe_instances()["Reservations"]:
    for each_instance in each_reservation["Instances"]:
        print(each_instance["InstanceId"])

# List all S3 buckets in us-east-1 region.

print(f"The S3 buckets in the us-east-1 region are as below:")
for each_bucket in s3_aws_service.list_buckets()["Buckets"]:
    print(each_bucket["Name"])