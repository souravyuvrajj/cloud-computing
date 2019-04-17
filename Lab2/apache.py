import os
import subprocess

print("****\nscript to install Apache in ec2 Instance\n\n****")
os.system("sudo yum -y install httpd")
os.system("sudo service httpd start ")

#scp -i part22.py ec2-user@ec2-13-232-122-192.ap-south-1.compute.amazonaws.com:~/
#ssh -i "sourav.pem" ec2-user@ec2-35-154-22-33.ap-south-1.compute.amazonaws.com
#sudo systemctl start httpd
#sudo systemctl status httpd
#sudo easy install pip
