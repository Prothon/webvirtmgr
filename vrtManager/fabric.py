import fabric

class fabrictests():
    def uptime(self):
        local('uname -s')