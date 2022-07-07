'''
Base cfg host name, time serv, firewall, Hardware flow
'''


import re
import yaml
import netmiko
from pprint import pprint
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)

def base_cfg(device, commands,log = True):
    if log:
        print(f"Connect to {device['host']}...")
    result = {}
    try:
        with ConnectHandler(**device) as ssh:
            print(device['host'], "connected")
            for command in commands:
                output = ssh.send_command(command)
                if "" in output:
                    output = "command passed"
                    result[command] = output
                else:
                    output = "bad command"
                    result[command] = output
        return result
    except (NetmikoAuthenticationException, NetmikoTimeoutException) as error:
        pprint("*"*20, "ERROR", "*"*20)


if __name__ == "__main__":
        commands = [
        "uci set system.@system[0].hostname='DUT'",
        "uci set system.ntp.server='0.ntp2.stratum2.ru'",
        "uci set firewall.@zone[1].forward='ACCEPT'",
        "uci set firewall.@zone[1].input='ACCEPT'",
        "uci set firewall.@defaults[0].flow_offloading='1'",
        "uci set firewall.@defaults[0].flow_offloading_hw='1'",
        "uci commit"
        ]
        with open("BM10_LTE.yaml") as f:
            device = yaml.safe_load(f)
            for dev in device:
                pprint(base_cfg(dev, commands))






