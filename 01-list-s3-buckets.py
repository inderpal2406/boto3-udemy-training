# Import modules.

import boto3

# Get the S3 bucket list.

aws_console = boto3.session.Session(profile_name="inderpalaws02-s3-admin")
aws_resource = aws_console.resource("s3")

for each_bucket in aws_resource.buckets.all():
    print(each_bucket.name)
