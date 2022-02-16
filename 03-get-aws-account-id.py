# This script will display the AWS account id.

# Import modules.

import boto3

# Initiate AWS session.

aws_session = boto3.session.Session(profile_name="inderpalaws02-aws-admin")

# Create STS client from aws session.

sts_client = aws_session.client(service_name="sts",region_name="us-east-1")
print("The AWS account id is: ",sts_client.get_caller_identity().get("Account"))
#print(f"The AWS account id is: {sts_client.get_caller_identity().get('Account')}") 
#Above commented line also works, but the Account key of dictionary has to be mentioned in ''. If mentioned in "", it gives error.
