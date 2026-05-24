import logging
import boto3
from botocore.exceptions import ClientError
import os

def list_buckets():
    list = []
    s3 = boto3.resource('s3')
    for bucket in s3.buckets.all():
        list.append(bucket.name)
        # print(list)
    return list

def list_files(bucket, search_prefix="", token=None):
    client = boto3.client("s3")

    
    kwargs = {
        "Bucket": bucket,
        "MaxKeys": 12
    }
    
    if search_prefix:
        kwargs["Prefix"] = search_prefix
    if token:
        kwargs["ContinuationToken"] = token

    try:
        response = client.list_objects_v2(**kwargs)
        
        file_list = []
        if "Contents" in response:
            for each in response["Contents"]:
                file_list.append(each["Key"])
        
        next_token = response.get("NextContinuationToken", None)
        
        return file_list, next_token
    except Exception as e:
        import logging
        logging.error(e)
        return [], None

def upload_file(file_name, bucket, object_name=None):
    p = "file/"+file_name
    if object_name is None:
        object_name = os.path.basename(p)
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

def bucket_exists(bucket_name):
    client = boto3.client('s3')
    try:
        client.head_bucket(Bucket=bucket_name)
        return True
    except ClientError :
        return False
