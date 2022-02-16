# Import modules.

import boto3

# Get the IAM user list.

aws_console = boto3.session.Session(profile_name="inderpalaws02-iam-admin")
aws_resource = aws_console.resource("iam")

for each_user in aws_resource.users.all():
    print(each_user.name)
