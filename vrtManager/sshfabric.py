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

class FabricSupport:
    def __init__ (self):
        pass

    def run(self, host, port, command):
        env.host_string = "%s:%s" % (host, port)
        run(command)