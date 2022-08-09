import yaml
import netmiko
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)

class BwosSSH:
    def __init__(self, device_type, host, username, password, timeout):
        self.ssh  = ConnectHandler(**device)

    def send_sh_command(self,command):
        temp = self.ssh.send_command(command)
        result = temp
        return result
if __name__ == "__main__":
    device = {
        "device_type": "linux",
        "host": "192.168.2.1",
        "username": "root",
        "password": "!128500",
        "timeout": "1"
    }
    r1 = BwosSSH(**device)
    print (r1.send_sh_command("uci show"))