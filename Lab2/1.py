import boto3


bucket_name=input("Enter bucket name : ")
filename=['test.html','pic.jpg']

s3 = boto3.client('s3')

for i in filename:
	s3.upload_file(i,bucket_name,i)

print ("Done")

#rm *.pyc
