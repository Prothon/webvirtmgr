#!/bin/bash

echo "This is for initial installation of the application. Currently heavily in beta"

yum -y install http://dl.fedoraproject.org/pub/epel/6/i386/epel-release-6-8.noarch.rpm
yum -y install git python-pip libvirt-python libxml2-python python-websockify supervisor nginx 
yum install -y gcc python-devel python-setuptools


 iptables-save
iptables -I INPUT -p tcp --dport 80 -j ACCEPT
iptables -I INPUT -p tcp --dport 443 -j ACCEPT
/etc/init.d/iptables save
/etc/init.d/iptables restart 
