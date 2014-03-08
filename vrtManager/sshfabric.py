#!/usr/bin/python

import paramiko
import cmd

class RunCommand(object):
    def connect(self, hostip, username, password, port, command):
        """Connect to all hosts in the hosts list"""
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostip, username = username, password = password, port=port)
        (stdin, stdout, stderr) = client.exec_command(command)
        stdin.close()
        StandardOut = stdout.read()
        client.close()
        return StandardOut
