from fabric import api as fab
#from fabric.network import disconnect_all
from contextlib import contextmanager

def get_hostname(request):  
    hostname = f.remote_server(hostname)
    return hostname