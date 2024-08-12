# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import os
import json
from modules.menu_messages import *
from modules.config_loader import *
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError


def setup_session():

    # Get key-id and access-key.
    credentials_choice = ask_credentials()
    credentials_result, credentials = load_credentials(credentials_choice)

    # Get region_name and output format.
    config_choice = ask_config()
    config_result, config = load_config(config_choice)

    if not credentials_result:
        return 'CREDENTIALS ERROR!'

    elif not config_result:
        return 'CONFIG ERROR!'

    else:
        session = boto3.Session(
            aws_access_key_id=credentials['key_id'],
            aws_secret_access_key=credentials['access_key'],
            region_name=config['region']
        )
        return session


if __name__ == '__main__':

    session = setup_session()

    # Get service type.
    service = ask_aws_service()

    while service:

        # EC2 Service block
        if service == 'ec2':
            ec2 = session.client(service)

            ec2_instances = ec2.describe_instances()['Reservations'][0]['Instances']

            instance_index, instance_name, instance_id = ask_ec2_id(ec2_instances)

            action = ask_ec2_action()

            clear_screen()

            # Begin START Block
            if action == 'start' and ec2_instances[instance_index]['State']['Name'] == 'stopped':
                try:
                    response = ec2.start_instances(InstanceIds=[instance_id])  # InstanceIds receives a list
                    print(f'Starting instance {instance_name} - [{instance_id}]')

                except:  # specify except
                    print('error starting')
            elif action == 'start' and ec2_instances[instance_index]['State']['Name'] != 'stopped':
                print(f"Instance {instance_name} - [{instance_id}] is "
                      f"{ec2_instances[instance_index]['State']['Name']}.")
                print("Cannot start instance")
            # End START Block

            # Begin STOP Block
            elif action == 'stop' and ec2_instances[instance_index]['State']['Name'] == 'running':
                try:
                    response = ec2.stop_instances(InstanceIds=[instance_id])
                    print(f'Stopping instance {instance_name} - [{instance_id}]')
                except:  # specify except
                    print('error stopping')

            elif action == 'stop' and ec2_instances[instance_index]['State']['Name'] != 'running':
                print(f"Instance {instance_name} - [{instance_id}] is "
                      f"{ec2_instances[instance_index]['State']['Name']}.")
                print("Cannot stop instance")
            # End STOP Block

            # Begin REBOOT Block
            elif action == 'reboot' and ec2_instances[instance_index]['State']['Name'] == 'running':
                try:
                    response = ec2.reboot_instances(InstanceIds=[instance_id])
                    print(f'Rebooting instance {instance_name} - [{instance_id}]')
                except:  # specify except
                    print('error rebooting')

            elif action == 'reboot' and ec2_instances[instance_index]['State']['Name'] != 'running':
                print(f"Instance {instance_name} - [{instance_id}] is "
                      f"{ec2_instances[instance_index]['State']['Name']}.")
                print("Cannot reboot instance")
            # End REBOOT Block

            # Begin INSTANCE_STATUS Block
            elif action == 'instance_status':
                print(f"Instance {instance_name} - [{instance_id}] is "
                      f"{ec2_instances[instance_index]['State']['Name']}.")
            # End INSTANCE_STATUS Block

        sleep(5)
        clear_screen()
        service = ask_aws_service()
