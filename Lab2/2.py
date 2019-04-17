import boto3
import botocore

BUCKET_NAME=input("Enter bucket name : ")
KEY=input("Enter filename to download : ")


s3 = boto3.resource('s3')

try:
    s3.Bucket(BUCKET_NAME).download_file(KEY, KEY)
    print ("Done")
except botocore.exceptions.ClientError as e:
    if e.response['Error']['Code'] == "404":
        print("The object does not exist.")
    else:
        raise
