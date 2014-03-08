#from django.utils.timezone import utc
import fabric
from fabric.context_managers import hide, settings
from fabric.decorators import task, serial
from fabric.operations import run, sudo, local
from fabric.state import env
from fabric.tasks import execute
import datetime
import threading
import traceback

class ssh_connect(object):
    def get_hostname(self, uri, cmd):  
        execute(cmd, hosts=uri)
        return hostname

    def uptime(self):
        local(uptime)