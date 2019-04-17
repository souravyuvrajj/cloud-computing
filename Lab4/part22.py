import boto3
from botocore.client import Config

BUCKET_NAME='aws-container-lab2'
k=['test.html']


s3 = boto3.resource(
    's3',
    aws_access_key_id='AKIAJERTBDC5Y7HANPGA',
    aws_secret_access_key='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',
    config=Config(signature_version='s3v4')
)
for KEY in k:
	s3.Bucket(BUCKET_NAME).download_file(KEY,KEY)

print ("Done")
