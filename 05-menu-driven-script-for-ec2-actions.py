# This script will provide a menu of actions which can be taken on an ec2 instance.

# Import modules.

import boto3

# Display purpose of the script.

print(f"This script will ask for which action to be performed on an EC2 instance & take that action.\n")

# Initiate AWS session with ec2-admin profile.

aws_session = boto3.session.Session(profile_name="inderpalaws02-ec2-admin")

# Initiate EC2 service client.

ec2_client = aws_session.client(service_name="ec2",region_name="us-east-1")

# Display the menu of options.

while True:
    print(f"""
    The menu of options is as below,
    1. Start
    2. Stop
    3. Restart
    4. Terminate
    5. Exit
    """)
    # Ask for the option.
    user_choice = int(input("Enter your option [1|2|3|4|5]: "))
    if user_choice == 1:
        # Ask for the instance id.
        instance_id = input("Enter the instance id: ")
        print(f"Starting the instance... This'll take few minutes...")
        response = ec2_client.start_instances(InstanceIds=[instance_id])
    elif user_choice == 2:
        instance_id = input("Enter the instance id: ")
        print(f"Stopping the instance... This'll take few minutes...")
        response = ec2_client.stop_instances(InstanceIds=[instance_id])
    elif user_choice == 3:
        instance_id = input("Enter the instance id: ")
        print(f"Restarting the instance... This'll take few minutes...")
        response = ec2_client.reboot_instances(InstanceIds=[instance_id])
    elif user_choice == 4:
        instance_id = input("Enter the instance id: ")
        print(f"Terminating the instance... This'll take few minutes...")
        response = ec2_client.terminate_instances(InstanceIds=[instance_id])
    elif user_choice == 5:
        print(f"Exiting the script...")
        exit(0)
    else:
        print(f"Invalid option. Please enter [1|2|3|4|5] only.")
