import boto3

ec2 = boto3.resource('ec2')

for instance in ec2.instances.all():
	print (instance.id, instance.state)


instances = ec2.instances.filter(
    Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
for instance in instances:
    print("The running instance:->",instance.id, instance.instance_type)
