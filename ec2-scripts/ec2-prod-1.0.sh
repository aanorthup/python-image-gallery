#!/usr/bin/bash
export IMAGE_GALLERY_SCRIPT_VERSION="1.0"

# Install packages

yum -y update 
yum install -y python3 git postgresql postgresql-devel gcc python3-devel 
amazon-linux-extras install -y nginx1

# Configure/install custom software
cd /home/ec2-user
git clone https://github.com/aanorthup/python-image-gallery 
chown -R ec2-user:ec2-user python-image-gallery 
su ec2-user -l -c "cd ~/python-image-gallery && pip3 install -r requirements.txt --user"

# Start/enable services
systemctl stop postfix 
systemctl disable postfix 
systemctl start nginx 
systemctl enable nginx

su ec2-user -l -c "cd ~/python-image-gallery && ./start" >/var/log/image_gallery.log 2>&1 &
