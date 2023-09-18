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
    

def check_route_ripv2():
    try:
        temp = r1.send_sh_command(device, "ip route")
        if "200.1.20.0/24 via 192.168.20.2" in temp:
            print("Ip route to host ok!")
            return True
        else:
            return False
    except ValueError as err:
        return False


def check_ping_interf200(ip_for_ping): # check ping neighbor
    try:

        res_ping_inet = r1.ping_ip(device)
        print(res_ping_inet)
        if "destination available" in res_ping_inet:
            print("Interface 200 availeble, RIP OK")
            return True
        else:
            print("Interface 200- not available, RIP bad ")
            return False
    except ValueError as err:
        return False


def check_ping_interf(ip_for_ping): # check ping Internet
    try:
        res_ping_inet = r1.ping_ip(device,ip_for_ping)
        print(res_ping_inet)
        if "destination available" in res_ping_inet:
            print("Interface availeble, RIPv2 OK")
            return True
        else:
            print("Interface is not available, RIPv2 bad ")
            return False
    except ValueError as err:
        return False
    
if __name__ == "__main__":
    result = check_ping_interf200(ip_for_ping='200.1.10.2')
    print(result)