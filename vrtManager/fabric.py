from fabric.api import run, local, hosts, cd
from fabric.contrib import django

def host_type():
    run('uname -s')