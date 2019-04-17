import boto3

print ("Connecting to EC2")

ec2 = boto3.resource('ec2')

#MinCount and MaxCount: Specify the number of instances to establish
#ImageID: This specifies the instance we want to create.
#InstanceType: The size of the instance to create.
instances = ec2.create_instances(
	ImageId='ami-00b6a8a2bd28daf19',
	MinCount=1,
	MaxCount=1,
	KeyName="sourav",
	InstanceType="t2.micro",
	SecurityGroupIds =['sg-0b65e951dea92f0ce']
)

for instance in instances:
    print(instance.id, instance.instance_type," is running")
