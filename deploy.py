import argparse
import os
from subprocess import call, PIPE

parser = argparse.ArgumentParser(
    description='A small script to deploy the imageService lambda'
)

parser.add_argument('-u', '--update', help='Updates the lambda_handler\'s code', action="store_true")
parser.add_argument('-p', '--package', help='Update the packages', action="store_true")
parser.add_argument('-d', '--deploy', help='Deploy the lambda to AWS', action="store_true")

parser.add_argument('-l', '--lambda-name', help='Change the name of the lambda being deployed. Default: imageService')
parser.add_argument('-s', '--source-file', help='Change the name of the source file deployed. Default: image_service.py')
parser.add_argument('-z', '--zip-file', help='Change the name of the zip file being updated. Default: function.zip')
parser.add_argument('-r', '--profile_name', help='Change the name of the profile to execute the AWS command. Default: personal')

args = parser.parse_args()


LAMBDA_NAME = args.lambda_name or 'imageService'
SOURCE_NAME = args.source_file or 'image_service.py'
ZIP_NAME = args.zip_file or 'function.zip'
PROFILE = args.profile_name or 'personal'


def call_command(command):
    source_dir = os.getcwd()
    call(command.split(), stdout=PIPE, cwd=source_dir)

if args.update:
    command = f'zip -g ./{ZIP_NAME} ./{SOURCE_NAME}'
    print(f'Updating {ZIP_NAME} to contain updated source file {SOURCE_NAME}')
    print(f'{command}\n')
    call_command(command)


if args.package:
    command = f'zip -r9 ./{ZIP_NAME} ./packages'
    print(f'Packaging {ZIP_NAME} to contain packages in ./packages')
    print(f'{command}\n')
    call_command(command)


if args.deploy:
    command = f'aws lambda update-function-code --function-name {LAMBDA_NAME} --zip-file fileb://{ZIP_NAME} --profile personal'
    print(f'Deploying {LAMBDA_NAME} to AWS from zip {ZIP_NAME}')
    print(f'{command}\n')
    call_command(command)
