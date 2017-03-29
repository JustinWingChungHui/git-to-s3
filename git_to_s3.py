
"""
Module to download git repo and upload it to Amazon s3

Configure the bucket, and git url using the settings file

Ths also requires AWS credentials to be set up in a file (or using AWS CLI):

Unix: ~/.aws/credentials
Windows: C:\\Users\\Username\\.aws\\credentials

In this file put the following:

[default]
aws_access_key_id = YOUR_ACCESS_KEY
aws_secret_access_key = YOUR_SECRET_KEY

[default]
region=us-east-1

"""

import os
import boto3
import settings
import shutil
import errno, stat
from os import listdir
from os.path import isdir
from mimetypes import MimeTypes
from git import Repo

def upload_file(file):
    """
    uploads a file to s3
    """
    print("Uploading %s" % file)

    #Get the mime type of the file
    mime = MimeTypes()
    mime_type = mime.guess_type(file)[0]

    data = open(file, 'rb')

    local_key = file.replace(settings.TEMP_DIRECTORY, "")

    # Replace windows slashes with unix slashes
    key = local_key.replace("\\", "/")

    # Remove first /
    if key.startswith("/"):
        key = key[1:]

    storage_service = boto3.resource('s3')

    if mime_type:
        storage_service.Object(settings.AWS_STORAGE_BUCKET_NAME, key).put(
            Body=data,
            ContentType=mime_type)
    else:
        # Use default mime type
        storage_service.Object(settings.AWS_STORAGE_BUCKET_NAME, key).put(
            Body=data)



def upload_dir(path):
    """
    Uploads directory recursively to s3
    """
    for file in listdir(path):

        filepath = os.path.join(path, file)
        if isdir(filepath) is True:
            upload_dir(filepath)
        else:
            upload_file(filepath)



def remove_readonly(func, path, excinfo):
    """
    Changes permissions on files that can't be deleted
    by shutil.rmtree
    """
    os.chmod(path, stat.S_IWRITE)
    func(path)




try:
    # Create temp directory
    print("Creating temporary directory %s" % settings.TEMP_DIRECTORY)
    if not os.path.exists(settings.TEMP_DIRECTORY):
        os.makedirs(settings.TEMP_DIRECTORY)

    # Clone repository to temp directory
    print("Cloning repository from %s" % settings.GIT_URL)
    Repo.clone_from(settings.GIT_URL, settings.TEMP_DIRECTORY)

    # Uploads contents of temp directory to s3
    print("Uploading to S3")
    upload_dir(settings.TEMP_DIRECTORY)

except Exception as ex:
    print(ex)

finally:
    # Deletes temporary directory
    print("Deleting temporary directory and contents")
    shutil.rmtree(settings.TEMP_DIRECTORY, onerror=remove_readonly)
