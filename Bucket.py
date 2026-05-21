import logging
import boto3
from botocore.exceptions import ClientError
import os

def list_buckets():
    list = []
    s3 = boto3.resource('s3')
    for bucket in s3.buckets.all():
        list.append(bucket.name)
    return list

def list_files(bucket):
    list = []
    client = boto3.client("s3")

    paginator = client.get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=bucket):
        for each in page["Contents"]:
            list.append(each["Key"])
        return list




def upload_file(file_name, bucket, object_name=None):
    p = "file/"+file_name
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(p)

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(p, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    os.remove(p)
    return True

def download_file(file_name, bucket, output):
    s3 = boto3.client("s3")
    s3.download_file(bucket, file_name, output)

def delete_file(file_name, bucket):
    s3 = boto3.client('s3')
    s3.delete_object(Bucket=bucket, Key=file_name)

if __name__ == "__main__":
    list_files("aa-ynov-intro")