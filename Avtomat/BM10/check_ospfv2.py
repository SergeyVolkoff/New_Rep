
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



def check_route_ospfv2_net():
    # ф-я в цикле переберет список маршрутов, если нужного нет - вернет false
    try:
        return_ip_route = r1.send_sh_command(device, "ip route")
        list_iproute=('192.168.10.0/24',
                      '192.168.20.0/24',
                      '200.1.10.0/24 ',
                      '200.1.20.0/24 ',
                     
                      )
        i=0
        for ip in list_iproute:
            if ip  in return_ip_route:
                i+=1
                print(f"Ip route {ip} ok!",i)
            else:
                if ip  not in return_ip_route:
                    print(f"No ip route {ip} ")
        if i==4:
            return True
        else:
            return False
    except ValueError as err:
        return False
    

def check_ping_interf(ip_for_ping): # check ping Internet
    try:
        res_ping_inet = r1.ping_ip(device,ip_for_ping)
        print(res_ping_inet)
        if "destination available" in res_ping_inet:
            print("Interface availeble, OSPFv2 OK")
            return True
        else:
            print("Interface is not available, OSPFv2 bad ")
            return False
    except ValueError as err:
        return False
    