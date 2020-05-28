import boto3
import json
import os

secret = {}
credentials = {}
try:
    secret = json.loads(open('credentials.json').read())
except FileNotFoundError as err:
    print('FileNotFoundError')
    
    # AWS
    secret['aws_access_key_id'] = ''
    secret['aws_secret_access_key'] = ''
    secret['aws_region_name'] = ''
    secret['aws_bucket_name'] = ''

def read_AWS_credentials():
    try:
        return secret['aws_region_name'], secret['aws_access_key_id'], secret['aws_secret_access_key']
    except Exception as e:
        print("Error reading AWS credentials: " + str(e))
        exit(1)

# get regions
def get_region():
    aws_region, _, _ = read_AWS_credentials()
    return aws_region

# connect to S3 service
def connect_s3():
    aws_region, aws_access_key, aws_secret_key = read_AWS_credentials()
    return connect_to_service("s3", aws_region, aws_access_key, aws_secret_key)

# connect to arbitrary service
def connect_to_service(service_name, region, access_key, secret_key):
    try:
        # authenticate
        client = boto3.client(service_name, region_name=region, aws_access_key_id=access_key, aws_secret_access_key=secret_key)
        return client
    except Exception as e:
        print("Error connecting to AWS: " + str(e))
        exit(1)

def get_s3_buckets(s3_client):
    buckets_field = "Buckets"
    buckets_name_field = "Name"

    try:
        buckets_response = s3_client.list_buckets()
        bucket_names = []

        if buckets_field not in buckets_response:
            raise Exception("Response not listed successfully.")

        for bucket in buckets_response[buckets_field]:
            if buckets_name_field not in bucket:
                print("Malformed bucket: " + bucket)
                continue
            bucket_names.append(bucket[buckets_name_field])
            print(bucket[buckets_name_field])
        return bucket_names
    except Exception as e:
        print("Error receiving buckets list: " + str(e))
        exit(1)


# get all S3 files in list of buckets
def get_all_s3_files_and_folders(s3_client, all_buckets):
    all_content = []
    for i in range(0, len(all_buckets)):
        bucket = all_buckets[i]
        content = get_s3_bucket_contents(s3_client, bucket)
        all_content.append({"bucket":bucket, "content":content})	
    return all_content

# get all standard files in the bucket
def get_s3_bucket_contents(s3_client, bucket_name):
    contents_field="Contents"
    bucket_contents = []

    try:
        response = s3_client.list_objects(Bucket = bucket_name)
        if contents_field not in response:
            # means it's not a file bucket
            return bucket_contents

        contents = response[contents_field]
        for i in range(0, len(contents)):
            bucket_contents.append(contents[i]["Key"])
        return bucket_contents
            
    except Exception as e:
        print("Error listing all files in bucket: " + bucket_name + " - " + str(e))
        return []

# download file from bucket
def download_s3_file(s3_client, bucket_name, file_name):
    try:
        make_file_path(file_name)

        with open(file_name, 'wb') as data:
            s3_client.download_fileobj(bucket_name, file_name, data)
        return True
    except Exception as e:
        print("Failed to download file: " + bucket_name + " - " + file_name + " - " + str(e))
        return False


# make a local directory for file if required
def make_file_path(file_name):
    if not os.path.exists(os.path.dirname(file_name)):
        try:
            os.makedirs(os.path.dirname(file_name))
        except Exception as err: # Guard against race condition
            print("Error make_file_path Guarding against race condition:" + str(err))
            return

# download file from bucket
def upload_s3_file(s3_client, bucket_name, file_name):
    try:
        with open(file_name, 'rb') as data:
            s3_client.upload_fileobj(data, bucket_name, file_name)
        return True
    except Exception as e:
        print("Failed to upload file: " + bucket_name + " - " + file_name + " - " + str(e))
        return False

# download files from bucket
def download_s3_files(s3_client, bucket_name, file_names):
    for i in range(0, len(file_names)):
        download_s3_file(s3_client, bucket_name, file_names[i])

# upload file
def upload_s3_files(s3_client, bucket_name, file_names):
    for i in range(0, len(file_names)):
        upload_s3_file(s3_client, bucket_name, file_names[i])


def get_presigned_url(s3_client, file_name, bucket_name="birthday-engine"):
    # contentType = file_name.split('.').pop()
    return s3_client.generate_presigned_post(
        Bucket=bucket_name,
        Key=file_name,
        Fields={"acl": "public-read"},
        Conditions=[
            {"acl": "public-read"}
        ],
        ExpiresIn=3600
    )
# "Content-Type": "png"
# {"Content-Type": "png"}
