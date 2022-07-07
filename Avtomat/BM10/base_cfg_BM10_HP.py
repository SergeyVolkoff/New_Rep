'''
Base cfg host name, time serv, firewall
'''


import re
import yaml
import netmiko
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)

def base_cfg(device, command,log = True):
    if log:
        print(f"Connect to {device['host']}...")
    result = ""
    try:
        with ConnectHandler(**device) as ssh:
            print(device['host'], "connected")
            temp = ssh.send_config_set(commands)
            for com in commands:
                if "root@BWOS:~#" in temp:
                    result = "Ok"
        return result
    except (NetmikoAuthenticationException, NetmikoTimeoutException) as error:
        print("*"*20, "ERROR", "*"*20)


if __name__ == "__main__":
        commands = [
        "uci set system.@system[0].hostname='DUT'",
        "uci set system.ntp.server='0.ntp2.stratum2.ru'",
        "uci commit"
        ]
        with open("BM10_LTE.yaml") as f:
            device = yaml.safe_load(f)
            for dev in device:
                print(base_cfg(dev, commands))






