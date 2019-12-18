
import os
import boto3
import sys
import traceback
import time

ec2 = boto3.resource('ec2')
imageami = input('Enter AMI Image you want to spin up: ')
string_value = str(imageami)
ami_count = input('number of instances: ')
ami_count_int = int(ami_count)
name_plo = input('policy name: ')
mysg = ec2.create_security_group(GroupName=name_plo,Description='testme')
mysg.authorize_ingress(IpPermissions=[
            {'IpProtocol': 'tcp',
             'FromPort': 80,
             'ToPort': 80,
             'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
            {'IpProtocol': 'tcp',
             'FromPort': 22,
             'ToPort': 22,
             'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
        ])
user_data_packages='''
#!/bin/bash 
sudo yum -y update
sudo yum install -y htop
sudo yum install -y vim
sudo useradd aaron
sudo usermod -a -G wheel,adm aaron
echo -e 'password\npassword\n' | sudo passwd ec2-user
echo -e 'password\npassword\n' | sudo passwd aaron
echo -e 'password\npassword\n' | sudo passwd root
wget -O splunkforwarder-8.0.0-1357bef0a7f6-linux-2.6-x86_64.rpm 'https://www.splunk.com/bin/splunk/DownloadActivityServlet?architecture=x86_64&platform=linux&version=8.0.0&product=universalforwarder&filename=splunkforwarder-8.0.0-1357bef0a7f6-linux-2.6-x86_64.rpm&wget=true'
sudo rpm -i splunkforwarder-8.0.0-1357bef0a7f6-linux-2.6-x86_64.rpm
sudo DD_API_KEY=8b47966137e9f64b6005e591020698e8 bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"
sudo yum install -y git
sudo yum install -y sshpass
sudo yum install -y python
cd /home/ec2-user/
git clone https://github.com/aaronjameshorne/python.git
sudo yum install epel-release
sudo yum -y update
cat << DD > /etc/ssh/sshd_config
#       $OpenBSD: sshd_config,v 1.100 2016/08/15 12:32:04 naddy Exp $

# This is the sshd server system-wide configuration file.  See
# sshd_config(5) for more information.

# This sshd was compiled with PATH=/usr/local/bin:/usr/bin

# The strategy used for options in the default sshd_config shipped with
# OpenSSH is to specify options with their default value where
# possible, but leave them commented.  Uncommented options override the
# default value.

# If you want to change the port on a SELinux system, you have to tell
# SELinux about this change.
# semanage port -a -t ssh_port_t -p tcp #PORTNUMBER
#
#Port 22
#AddressFamily any
#ListenAddress 0.0.0.0
#ListenAddress ::

HostKey /etc/ssh/ssh_host_rsa_key
#HostKey /etc/ssh/ssh_host_dsa_key
HostKey /etc/ssh/ssh_host_ecdsa_key
HostKey /etc/ssh/ssh_host_ed25519_key

# Ciphers and keying
#RekeyLimit default none

# Logging
#SyslogFacility AUTH
SyslogFacility AUTHPRIV
#LogLevel INFO

# Authentication:

#LoginGraceTime 2m
PermitRootLogin yes
#StrictModes yes
#MaxAuthTries 6
#MaxSessions 10

PubkeyAuthentication yes

# The default is to check both .ssh/authorized_keys and .ssh/authorized_keys2
# but this is overridden so installations will only check .ssh/authorized_keys
AuthorizedKeysFile .ssh/authorized_keys

#AuthorizedPrincipalsFile none


# For this to work you will also need host keys in /etc/ssh/ssh_known_hosts
#HostbasedAuthentication no
# Change to yes if you don't trust ~/.ssh/known_hosts for
# HostbasedAuthentication
#IgnoreUserKnownHosts no
# Don't read the user's ~/.rhosts and ~/.shosts files
#IgnoreRhosts yes

# To disable tunneled clear text passwords, change to no here!
PasswordAuthentication yes
#PermitEmptyPasswords no
#PasswordAuthentication no

# Change to no to disable s/key passwords
#ChallengeResponseAuthentication yes
ChallengeResponseAuthentication no

# Kerberos options
#KerberosAuthentication no
#KerberosOrLocalPasswd yes
#KerberosTicketCleanup yes
#KerberosGetAFSToken no
#KerberosUseKuserok yes

# GSSAPI options
GSSAPIAuthentication yes
GSSAPICleanupCredentials no
#GSSAPIStrictAcceptorCheck yes
#GSSAPIKeyExchange no
#GSSAPIEnablek5users no

# Set this to 'yes' to enable PAM authentication, account processing,
# and session processing. If this is enabled, PAM authentication will
# be allowed through the ChallengeResponseAuthentication and
# PasswordAuthentication.  Depending on your PAM configuration,
# PAM authentication via ChallengeResponseAuthentication may bypass
# the setting of "PermitRootLogin without-password".
# If you just want the PAM account and session checks to run without
# PAM authentication, then enable this but set PasswordAuthentication
# and ChallengeResponseAuthentication to 'no'.
# WARNING: 'UsePAM no' is not supported in Red Hat Enterprise Linux and may cause several
# problems.
UsePAM yes

#AllowAgentForwarding yes
#AllowTcpForwarding yes
#GatewayPorts no
X11Forwarding yes
#X11DisplayOffset 10
#X11UseLocalhost yes
#PermitTTY yes
#PrintMotd yes
#PrintLastLog yes
#TCPKeepAlive yes
#UseLogin no
#UsePrivilegeSeparation sandbox
#PermitUserEnvironment no
#Compression delayed
#ClientAliveInterval 0
#ClientAliveCountMax 3
#ShowPatchLevel no
#UseDNS yes
#PidFile /var/run/sshd.pid
#MaxStartups 10:30:100
#PermitTunnel no
#ChrootDirectory none
#VersionAddendum none

# no default banner path
#Banner none
DD
sudo systemctl restart sshd
sudo amazon-linux-extras install -y nginx1
sudo systemctl start nginx
sudo rm -f /usr/share/nginx/html/*.*
cd /usr/share/nginx/html
sudo git clone https://github.com/aaronjameshorne/ansible.git
cd  /usr/share/nginx/html/ansible/appointments
cp index.nginx-debian.html ../../
cp my_page.html ../../
sudo mv index.nginx-debian.html index.html
'''

def default_ami():
    try:
        instances = ec2.create_instances(
            ImageId='ami-0b2d8d1abb76a53d8',
            MinCount=ami_count_int,
            MaxCount=ami_count_int,
            InstanceType='t2.micro',
            NetworkInterfaces=[{'DeviceIndex': 0,'AssociatePublicIpAddress': True,'Groups':[mysg.group_id]}],
            KeyName='webapp',
            UserData=user_data_packages
    )
    except:
        errorFile = open('aws_log.txt','w')
        errorFile.write(traceback.format_exc())
        errorFile.close()
        print('Any errors will be logged to aws_log file')
def user_ami():
    try:
        instances = ec2.create_instances(
            ImageId=string_value,
            MinCount=ami_count_int,
            MaxCount=ami_count_int,
            InstanceType='t2.micro',
            NetworkInterfaces=[{'DeviceIndex': 0,'AssociatePublicIpAddress': True,'Groups':[mysg.group_id]}],
            KeyName='webapp'
    )
    except:
        errorFile = open('aws_log.txt','w')
        errorFile.write(traceback.format_exc())
        errorFile.close()
        print('Any errors will be logged to aws_log file')

if string_value == '':
    default_ami()
else: user_ami()
print('Wait for IPs to be return to connect....Take will take up to 3 mins....')
time.sleep(10)
print('Waiting on Ips..')
time.sleep(10)
print('Waiting on Ips......')
time.sleep(15)
print('Waiting on Ips...........')
time.sleep(15)
os.system('python3 info_ec2.py | grep Public | grep -v DnsName | grep -v Address')
