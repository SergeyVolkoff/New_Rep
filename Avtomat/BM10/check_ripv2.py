import re
import time
import yaml
import netmiko
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)
from clss_Router import Router
"""

"""
with open("BM10_LTE.yaml") as f:
    temp = yaml.safe_load(f)
    for t in temp:
        device = dict(t)
        r1 = Router(**device)

def check_enable_ripv2():
    try:
        temp = r1.send_sh_command(device, 'uci show rip.@rip[0].enabled')
        if "='1'" in temp:
            print("RIPv2 - enable!")
            return True
        else:
            return False
    except ValueError as err:
        return False

def check_ver_ripv2():
    try:
        temp = r1.send_sh_command(device, "uci show rip.@rip[0].version")
        if "='2'" in temp:
            print("RIP version is 2!")
            return True
        else:
            return False
    except ValueError as err:
        return False