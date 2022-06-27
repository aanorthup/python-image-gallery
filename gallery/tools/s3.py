import logging
import boto3
import json
from botocore.exceptions import ClientError


endpoint = "https://s3-us-east-1.amazonaws.com/edu.au.cc.aan.image-gallery/"


def create_bucket(bucket_name, region=None):
    """Create an S3 bucket in a specified region
    If a region is not specified, the bucket is created in the S3 default
    region (us-east-1).
    :param bucket_name: Bucket to create
    :param region: String region to create bucket in, e.g., 'us-west-2'
    :return: True if bucket created, else False
    """
    # Create bucket
    try:
        if region is None:
            s3_client = boto3.client('s3')
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client = boto3.client('s3', region_name=region)
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name,
                                    CreateBucketConfiguration=location)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def put_object(bucket_name, key, value):
    try:
        s3_client = boto3.client('s3')
        s3_client.put_object(Bucket=bucket_name, Key=key, Body=value)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def get_object(bucket_name, key):
    try:
        s3_resource = boto3.resource('s3')
        obj = s3_resource.Object(bucket_name, key)
        body = obj.get()['Body'].read()
    except ClientError as e:
        logging.error(e)
        return None
    return body


def upload_file(file, bucket, username):
    s3_client = boto3.client('s3')
    s3_client.upload_fileobj(file, bucket, str(username) + '/{}'.format(file.filename))

    return

def delete_object(bucket_name, key):
    try:
        s3_client = boto3.client('s3')
        response = s3_client.delete_object(Bucket=bucket_name, Key=key)
    except ClientError as e:
        logging.error(e)
        return None
    return response

def get_images_by_username(bucket, username):
    s3_client = boto3.resource('s3')
    all_images = []
    bucket = s3_client.Bucket(bucket)
    objects = bucket.objects.filter(Prefix= str(username) + '/')
    for obj in objects:
        key = obj.key
        url = 'https://s3.amazonaws.com/edu.au.cc.aan.image-gallery' + '/' + str(key)
        all_images.append(url)
    return all_images

def list_objects(bucket_name, name):
    try:
        s3_client = boto3.client('s3')
        result = s3_client.list_objects(Bucket=bucket_name, Prefix=name)
        list = result['Contents']
        images = []
        for i in list:
            images.append(endpoint + i['Key'])
    except ClientError as e:
        logging.error(e)
        return None
    return images


def create_presigned_url(bucket_name, object_name, expiration=3600):
    """Generate a presigned URL to share an S3 object

    :param bucket_name: string
    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """

    # Generate a presigned URL for the S3 object
    s3_client = boto3.client('s3')
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL
    return response


def get_url(bucket_name, object_name):
    url = create_presigned_url(bucket_name, object_name)
    if url is not None:
        response = requests.get(url)

# def main():
# put object in bucket


# if __name__ == '__main__':
#   main()

