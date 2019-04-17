import boto.ec2
import os
import subprocess
from boto.manage.cmdshell import sshclient_from_instance
conn=boto.ec2.connect_to_region('ap-south-1a')
instance = conn.get_all_instances(['i-070f5d4ed732eb5d8'])[0].instances[0]
ssh_client = sshclient_from_instance(instance,'sourav.pem',user_name='ec2-user')
print (ssh_client.run('sudo yum install -y httpd'))
print (ssh_client.run('sudo service httpd start'))
print (ssh_client.run('sudo pip install boto3'))
print (ssh_client.run('cat > part22.py'))
print (ssh_client.run('python part22.py'))
print (ssh_client.run('sudo mv test.html /var/www/html'))
print (ssh_client.run('sudo systemctl start httpd'))
print("done")
