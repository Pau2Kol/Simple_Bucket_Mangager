import io
import boto3
from botocore.exceptions import ClientError
import logging

def list_buckets():
    list_b = []
    s3 = boto3.resource('s3')
    for bucket in s3.buckets.all():
        list_b.append(bucket.name)
    return list_b

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
        logging.error(e)
        return [], None

def upload_file_memory(file_obj, bucket, object_name):
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_fileobj(file_obj, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def get_file_stream(file_name, bucket):
    s3 = boto3.client('s3')
    try:
        response = s3.get_object(Bucket=bucket, Key=file_name)
        buffer_memoire = io.BytesIO(response['Body'].read())
        return buffer_memoire
    except ClientError as e:
        logging.error(e)
        return None

def delete_file(file_name, bucket):
    s3 = boto3.client('s3')
    try:
        s3.delete_object(Bucket=bucket, Key=file_name)
    except ClientError as e:
        logging.error(e)

def bucket_exists(bucket_name):
    client = boto3.client('s3')
    try:
        client.head_bucket(Bucket=bucket_name)
        return True
    except ClientError:
        return False