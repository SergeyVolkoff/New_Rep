
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

def check_enable_ospfv2():
    try:
        temp = r1.send_sh_command(device, 'uci show ospf.@ospf[0].enabled')
        if "='1'" in temp:
            print("OSPFv2 - enable!")
            return True
        else:
            return False
    except ValueError as err:
        return False