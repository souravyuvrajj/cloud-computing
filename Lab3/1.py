import boto3

print ("Connecting to EC2")

ec2 = boto3.resource('ec2')

#MinCount and MaxCount: Specify the number of instances to establish
#ImageID: This specifies the instance we want to create.
#InstanceType: The size of the instance to create.
instances = ec2.create_instances(
	ImageId='ami-188fba77',
	MinCount=1,
	MaxCount=1,
	KeyName="sourav",
	InstanceType="t2.micro",
	SecurityGroupIds =['sg-0b65e951dea92f0ce']
)
ids =[]
print 'Running instances are \n'
instances = ec2.instances.filter(
    Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
for instance in instances:
    print(instance.id, instance.instance_type)
    ids.append(instance.id)

print "Instance Status:\n"
for status in ec2.meta.client.describe_instance_status()['InstanceStatuses']:
    print(status)

print "Now stopping the running instances \n"
ec2.instances.filter(InstanceIds=ids).stop()
