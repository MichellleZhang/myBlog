import os
import boto3
from botocore.exceptions import ClientError
import logging

s3 = boto3.client('s3')
# create a bucket 
# bucket = s3.create_bucket(
#     Bucket = 'zqc-blog-resources',
#     CreateBucketConfiguration = {
#         'LocationConstraint': 'us-east-2'
#     }
# )
# all buckets
# buckets_resp = s3.list_buckets()
# for bucket in buckets_resp['Buckets']:
#     print(bucket)
# all objects in the bucket 
# response = s3.list_object_v2(Bucket = BUCKET_NAME)
# for obj in response["Contents"]:
#     print(obj)


BUCKET_NAME = 'zqc-blog-resources'
# upload file to bucket
# /test/test1.jpg -> 第一层/ 第二层test 第三层test1.jpg
# test/test1.jpg -> 第一层 test 第二层test1.jpg
# with open("/Users/zqc/Desktop/blogResoueces/about/travel.jpg", "rb") as f:
#     s3.upload_fileobj(f, BUCKET_NAME, "about/travel.jpg", ExtraArgs={"ACL":"public-read"})
# with open("/Users/zqc/Desktop/blogResoueces/about/foods.jpg", "rb") as f:
#     s3.upload_fileobj(f, BUCKET_NAME, "about/foods.jpg", ExtraArgs={"ACL":"public-read"})

with open("/Users/zqc/Desktop/blogResoueces/about/avatar.jpeg", "rb") as f:
    s3.upload_fileobj(f, BUCKET_NAME, "about/avatar.jpg", ExtraArgs={"ACL":"public-read"})
