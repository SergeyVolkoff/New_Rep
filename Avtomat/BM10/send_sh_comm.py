import re
import yaml
import netmiko
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)

def send_sh_comm(device, command_sh,log = True):
    if log:
        print(f"Connect to {device['host']}...")
    result = ""
    try:
        with ConnectHandler(**device) as ssh:
            print(device['host'], "connected")
            temp = ssh.send_config_set(command_sh)
        return temp
    except (NetmikoAuthenticationException, NetmikoTimeoutException) as error:
        print("*"*5, "Error connection to:", device['host'], "*"*5)

if __name__ == "__main__":
    command_sh = "uci show network.wan"
    with open("BM10_LTE.yaml")as f:
        device = yaml.safe_load(f)
        for dev in device:
            print(send_sh_comm(dev, command_sh))
