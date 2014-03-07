#!/bin/bash

git pull
chown -R nginx:nginx /var/www/webvirtmgr
/etc/init.d/supervisord restart
/etc/init.d/nginx restart