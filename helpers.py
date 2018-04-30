
import boto3

#This case works with PathStyle
#from botocore.client import Config

from config import S3_KEY, S3_SECRET, S3_BUCKET, S3_LOCATION

#These two are to have the ProgressPercetage
import os
import sys
import threading

#to get the presigned url
import requests


#This is to ensure no multipart uploads has long has the bandwith is not exceeded
from boto3.s3.transfer import TransferConfig

#Class that give you feedback regarding where is your uploading file
class ProgressPercentage(object):
    def __init__(self, filename):
        self._filename = filename
        self._size = float(os.path.getsize(filename))
        self._seen_so_far = 0
        self._lock = threading.Lock()
    def __call__(self, bytes_amount):
        #This is assumed to be hooked up to a single filename
        with self._lock:    
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size) * 100
            sys.stdout.write(
                "\r%s %s / %s (%.2f%%)" % (
                    self._filename, self._seen_so_far, self._size,
                    percentage
                )
            )
            sys.stdout.flush()

#path style
#s3 = boto3.client('s3', 'us-east-Nvirginia', config=Config(s3={'addressing_style': 'path'}))

#virtual enviroment 
s3 = boto3.client(
    's3',
    aws_access_key_id=S3_KEY,
    aws_secret_access_key=S3_SECRET
    )

MB = 1024 ** 3 # what would be the right operation for 

config = TransferConfig(multipart_threshold=8 * MB)

def upload_file_to_s3(file, bucket_name="memechat", acl="public-read"):
    try:
        #This is to get memes to the bucket
        s3.upload_fileobj(
            file,
            bucket_name,
            file.filename, # s3.upload_file("tmp.txt", "bucket-name", "key-name")
            #
            # Callback=ProgressPercentage(file),
            ExtraArgs={
                "ACL": acl, #this is canned ACL
                "ContentType": file.content_type
            }
        )
        #multiple ACL 
        '''    
        ExtraArgs={
        'GrantRead': 'uri="http://acs.amazonaws.com/groups/global/AllUsers"',
        'GrantFullControl': 'id="79a59df900b949e55d96a1e698fbacedfd6e09d98eacf8f8d5218e7cd47ef2be"',
        }
        '''

    except Exception as e:
        import pdb; pdb.set_trace()
        print("Something Happened: ", e)
        return e 

    return "{}{}".format(S3_LOCATION, file.filename)

# def download_file_from_s3(bucket_name, file , versionid= "my-version-id"):

#     (bucket_name, file.filename , file)


#Generating Presigned URLS, GET

def presigned_url_generator(file, bucket_name):

    url = s3.generate_presigned_url(
            ClientMethod='get_object',
            Params={
                'Bucket': bucket_name,
                'Key': 'key_name'
            }
            )
    return url 
    
    response = requests.get(url)
    return response  