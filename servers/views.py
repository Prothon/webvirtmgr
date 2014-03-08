import socket
import subprocess

import paramiko

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext

from servers.models import Compute
from instance.models import Instance
from servers.forms import ComputeAddTcpForm, ComputeAddSshForm
from vrtManager.hostdetails import wvmHostDetails
from vrtManager.connection import CONN_SSH, CONN_TCP, SSH_PORT, TCP_PORT
from vrtManager.sshfabric import RunCommand 
from libvirt import libvirtError


def index(request):
    """

    Index page.

    """
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login')
    else:
        return HttpResponseRedirect('/servers')


def servers_list(request):
    """
    Servers page.
    """
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login')

    def get_hosts_status(hosts):
        """
        Function return all hosts all vds on host
        """
        all_hosts = {}
        for host in hosts:
            try:
                socket_host = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                socket_host.settimeout(1)
                if host.type == CONN_SSH:
                    if ':' in host.hostname:
                        LIBVIRT_HOST, PORT = (host.hostname).split(":")
                        PORT = int(PORT)
                    else:
                        PORT = SSH_PORT
                        LIBVIRT_HOST = host.hostname
                    socket_host.connect((LIBVIRT_HOST, PORT))
                if host.type == CONN_TCP:
                    socket_host.connect((host.hostname, TCP_PORT))
                socket_host.close()
                status = 1
            except Exception as err:
                status = err
            all_hosts[host.id] = (host.name, host.hostname, status)
        return all_hosts

    computes = Compute.objects.filter()
    hosts_info = get_hosts_status(computes)
    form = None

    if request.method == 'POST':
        if 'host_del' in request.POST:
            compute_id = request.POST.get('host_id', '')
            try:
                del_inst_on_host = Instance.objects.filter(compute_id=compute_id)
                del_inst_on_host.delete()
            finally:
                del_host = Compute.objects.get(id=compute_id)
                del_host.delete()
            return HttpResponseRedirect(request.get_full_path())
        if 'host_tcp_add' in request.POST:
            form = ComputeAddTcpForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                new_tcp_host = Compute(name=data['name'],
                                       hostname=data['hostname'],
                                       type=CONN_TCP,
                                       login=data['login'],
                                       password=data['password'])
                new_tcp_host.save()
                return HttpResponseRedirect(request.get_full_path())
        if 'host_ssh_add' in request.POST:
            form = ComputeAddSshForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                new_ssh_host = Compute(name=data['name'],
                                       hostname=data['hostname'],
                                       type=CONN_SSH,
                                       login=data['login'])
                new_ssh_host.save()
                return HttpResponseRedirect(request.get_full_path())

    return render_to_response('servers.html', locals(), context_instance=RequestContext(request))


def infrastructure(request):
    """
    Infrastructure page.
    """
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login')

    compute = Compute.objects.filter()
    hosts_vms = {}

    for host in compute:
        try:
            socket_host = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket_host.settimeout(1)
            if host.type == CONN_SSH:
                socket_host.connect((host.hostname, SSH_PORT))
            if host.type == CONN_TCP:
                socket_host.connect((host.hostname, TCP_PORT))
            socket_host.close()
            status = 1
        except Exception:
            status = 2

        if status == 1:
            try:
                conn = wvmHostDetails(host, host.login, host.password, host.type)
                host_info = conn.get_node_info()
                host_mem = conn.get_memory_usage()
                hosts_vms[host.id, host.name, status, host_info[3], host_info[2],
                          host_mem['percent']] = conn.get_host_instances()
            except libvirtError as e:
                hosts_vms[host.id, host.name, 3, 0, 0, 0] = None
        else:
            hosts_vms[host.id, host.name, status, 0, 0, 0] = None

    return render_to_response('infrastructure.html', locals(), context_instance=RequestContext(request))

def cman(request):
    """
    cman page.
    """
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login')

    compute = Compute.objects.filter()
    #uptimetest = sshfabric.run("127.0.0.1", 22, uptime)
    #uptimetest = subprocess.Popen(['w'], stdout=subprocess.PIPE).communicate()[0] 
#    ssh = paramiko.SSHClient()
#    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#    ssh.connect('10.13.37.31', username='webvirtmgr', password='lol')
#    stdin, stdout, stderr = ssh.exec_command("hostname")
# Test
    ssh = RunCommand()
    stdout = ssh.connect('node1.prothon.lab','webvirtmgr','lol',22,"w")
    return render_to_response('cman.html', locals(), context_instance=RequestContext(request))
