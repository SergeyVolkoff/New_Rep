import yaml
import netmiko
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)

class BwosSSH:
    def __init__(self, device_type, host, username, password, timeout):
        ssh = ConnectHandler(**device)
        print(ssh)


if __name__ == "__main__":
    device = {
        "device_type": "linux",
        "host": "192.168.1.1",
        "username": "root",
        "password": "!128500",
        "timeout": "1"
    }
    r1 = BwosSSH(**device)
    print (r1.send_sh_command("uci show"))