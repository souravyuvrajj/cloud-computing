import boto.ec2
import boto.ec2.autoscale
from boto.ec2.autoscale import LaunchConfiguration
from boto.ec2.autoscale import AutoScalingGroup
from boto.ec2.cloudwatch import MetricAlarm
from boto.ec2.autoscale import ScalingPolicy
import boto.ec2.cloudwatch

access_key_id = "AKIAJERTBDC5Y7HANPGA"
secret_access_key = "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"

REGION = "ap-south-1"
AMI_ID = "ami-00b6a8a2bd28daf19"
EC2_KEY_HANDLE = "sourav"
INSTANCE_TYPE = "t2.micro"
SECGROUP_HANDLE = "launch-wizard-1"

print "Connecting to AutoScailing Service"

conn = boto.ec2.autoscale.connect_to_region(REGION, aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key)

print "Creating Launch configuration"

lc = LaunchConfiguration(name="My-Launch-Config-2",
		image_id=AMI_ID,
		key_name=EC2_KEY_HANDLE,
		instance_type=INSTANCE_TYPE,
		security_groups=[SECGROUP_HANDLE])

conn.create_launch_configuration(lc)

print "Creating auto-scaling group"

ag = AutoScalingGroup(group_name='My-Group',
		availability_zones=['ap-south-1a'],
		launch_config=lc,min_size=1,max_size=2,
		connection=conn)

conn.create_auto_scaling_group(ag)

print "Creating auto-scaling policies"

scale_up_policy = ScalingPolicy(name='scale_up',
			adjustment_type='ChangeInCapacity',
			as_name='My-Group',
			scaling_adjustment=1,
			cooldown=180)

scale_down_policy = ScalingPolicy(name='scale_down',
			adjustment_type='ChangeInCapacity',
			as_name='My-Group',
			scaling_adjustment=-1,
			cooldown=180)

conn.create_scaling_policy(scale_up_policy)
conn.create_scaling_policy(scale_down_policy)

scale_up_policy=conn.get_all_policies(as_group='My-Group',
	policy_names=['scale_up'])[0]
scale_down_policy=conn.get_all_policies(as_group='My-Group',
	policy_names=['scale_down'])[0]

print "Connecting to CloudWatch"

cloudwatch = boto.ec2.cloudwatch.connect_to_region(REGION)

alarm_dimensions={"AutoScalingGroupName":'My-Group'}


print "Creating scale-up alarm"

scale_up_alarm=MetricAlarm(
		name='scale_up_on_cpu',namespace='AWS/EC2',
		metric='CPUUtilization',statistic='Average',
		comparison='>',threshold='70',
		period='60',evaluation_periods=2,
		alarm_actions=[scale_up_policy.policy_arn],
		dimensions=alarm_dimensions)

cloudwatch.create_alarm(scale_up_alarm)

print "Connecting scale-down alarm"

scale_down_alarm=MetricAlarm(
		name='scale_down_on_cpu',namespace='AWS/EC2',
		metric='CPUUtilization',statistic='Average',
		comparison='<',threshold='50',
		period='60',evaluation_periods=2,
		alarm_actions=[scale_down_policy.policy_arn],
		dimensions=alarm_dimensions)

cloudwatch.create_alarm(scale_down_alarm)


print "Done"
