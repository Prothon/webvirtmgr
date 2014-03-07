#!/bin/bash

git pull
/etc/init.d/supervisord restart
/etc/init.d/nginx restart