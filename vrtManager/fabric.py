from fabric import run, local, hosts, cd
from fabric import django

def host_type():
    run('uname -s')