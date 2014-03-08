from django.utils.timezone import utc
from fabric.context_managers import hide, settings
from fabric.decorators import task, serial
from fabric.operations import run, sudo, local
from fabric.state import env
from fabric.tasks import execute
from skwissh.models import Server, Measure, MeasureDay, MeasureWeek, \
    MeasureMonth, CronLog
import datetime
import kronos
import threading
import traceback

def get_hostname(request):  
    execute(hostname, hosts=localhost)
    return hostname