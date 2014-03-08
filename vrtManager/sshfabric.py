#!/usr/bin/python

import paramiko
import cmd

class RunCommand(object):
    def connect(self, hostip, username, password, port):
        """Connect to all hosts in the hosts list"""
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostip, username = username, password = password, port=port)

    def run(self, command):
        """run Execute this command on all hosts in the list"""
        (stdin, stdout, stderr) = client.exec_command(command)
        stdin.close()
        return stdin, stdout, stderr

    def close(self, args):
        for conn in self.connections:
            conn.close()
