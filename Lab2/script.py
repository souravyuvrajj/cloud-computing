import boto3
from boto.manage.cmdshell import sshclient_from_instance
conn=boto3.resource('ec2')
instance = conn.get_all_instances(['i-064c1aca25ee9138a'])[0].instances[0]
print(instance)
ssh_client = sshclient_from_instance('i-064c1aca25ee9138a','sourav.pem',user_name='ec2-user')
print (ssh_client.run('sudo yum install -y httpd'))
