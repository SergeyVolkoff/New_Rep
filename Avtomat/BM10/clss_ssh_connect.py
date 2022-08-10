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
        self.ip = host
        self.name = username
        self.passwd = password
    def send_sh_command(self,command):
        temp = self.ssh.send_command(command)
        result = temp
        return result
if __name__ == "__main__":
    with open("BM10_LTE.yaml") as f:
        temp = yaml.safe_load(f)
        for t in temp:
            device = dict(t)
            r1 = BwosSSH(**device)
            print (r1.send_sh_command("uci show network"))  