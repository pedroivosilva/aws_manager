import os
import re
from pathlib import Path
import configparser
from getpass import getpass
from time import sleep


def credentials_from_file():

    home = Path(os.getenv('HOMEPATH'))
    aws_credentials_path = home / '.aws' / 'credentials'

    # Create a ConfigParser object
    config = configparser.ConfigParser()

    default_credentials = False
    aws_access_key_id = ''
    aws_secret_access_key = ''

    # Read the configuration file
    if aws_credentials_path.exists():
        credentials_file = True
        config.read(aws_credentials_path)
        if 'default' in config:
            aws_access_key_id = config['default']['aws_access_key_id']
            aws_secret_access_key = config['default']['aws_secret_access_key']
            default_credentials = True
        else:
            default_credentials = False
    else:
        credentials_file = False

    if credentials_file and default_credentials:
        return aws_access_key_id, aws_secret_access_key
    else:
        return False, False


def config_from_file():

    home = Path(os.getenv('HOMEPATH'))
    aws_config_path = home / '.aws' / 'config'

    # Create a ConfigParser object
    config = configparser.ConfigParser()

    default_config = False
    region = ''
    output = ''

    # Read the configuration file
    if aws_config_path.exists():
        config_file = True
        config.read(aws_config_path)
        if 'default' in config:
            region = config['default']['region']
            output = config['default']['output']
            default_config = True
        else:
            default_config = False
    else:
        config_file = False

    if config_file and default_config:
        return region, output
    else:
        return False, False


def validate_access_key_id(access_key_id):
    # AWS Access Key ID format: starts with AKIA or ASIA followed by 16 alphanumeric characters
    pattern_akia = r'^AKIA[0-9A-Z]{16}$'
    pattern_asia = r'^ASIA[0-9A-Z]{16}$'
    akia = re.match(pattern_akia, access_key_id)
    asia = re.match(pattern_asia, access_key_id)
    return (akia or asia) is not None


def validate_secret_access_key(secret_access_key):
    # AWS Secret Access Key format: 40 alphanumeric characters
    pattern = r'^[0-9A-Za-z/+=]{40}$'
    return re.match(pattern, secret_access_key) is not None


def validate_output_formats(output: str):
    # AWS formats:  json, text, table, or yaml
    formats = ['json', 'text', 'table', 'yaml']
    if output in formats:
        return True
    else:
        return False


def load_credentials(choice):
    # 1 = load from credentials file
    # 2 = Type manually
    if choice == 1:
        key_id, access_key = credentials_from_file()

        if not validate_access_key_id(key_id):
            return False, {'key_id': 'invalid key-id!', 'access_key': 'invalid key-id!'}
        elif key_id and access_key:
            return True, {'key_id': key_id, 'access_key': access_key}
        else:
            return False, {'key_id': 'No credentials file!', 'access_key': 'No credentials file!'}

    elif choice == 2:
        key_id = False
        access_key = False
        while not key_id and not access_key:
            key_id = str(input('Please enter your KEY ID: '))
            access_key = getpass('Please enter your ACCESS KEY: ')
            if not validate_access_key_id(key_id):
                key_id = False
                print('Please enter a valid KEY ID! (Ex: AKIAxxxxxxxxxxxxxxxx)\n')
                sleep(2)

        return True, {'key_id': key_id, 'access_key': access_key}


def load_config(choice):

    default_region = 'us-east-2'
    default_output = 'json'

    # 1 = load from config file
    # 2 = Type manually
    if choice == 1:
        region, output = config_from_file()

        if not validate_output_formats(output):
            return False, {'region': 'invalid output!', 'output': 'invalid output!'}
        elif region and output:
            return True, {'region': region, output: output}
        else:
            return False, {'region': 'No config file!', 'output': 'No config file!'}

    elif choice == 2:
        region = False
        output = False
        while not region and not output:
            region = str(input('Please enter AWS region: '))
            output = str(input('Please enter output format: '))
            if not validate_output_formats(output):
                output = False
                print('Please enter a valid output format! (json, text, table, yaml)\n')
                sleep(2)

        return True, {'region': region, output: output}

    elif choice == 3:
        region = True
        output = True
        return True, {'region': default_region, 'output': default_output}
