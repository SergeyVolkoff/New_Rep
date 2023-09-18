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


def check_enable_ripng():
    try:
        temp = r1.send_sh_command(device, 'uci show ripng.@rip[0].enabled')
        if "='1'" in temp:
            print("RIPng - enable!")
            return True
        else:
            return False
    except ValueError as err:
        return False
    

def check_route_ripng_net():
    # ф-я в цикле переберет список маршрутов, если нужного нет - вернет false
    try:
        return_ip_route = r1.send_sh_command(device, "ip -6 route")
        list_iproute=('2001:10::/64','2001:20::/64','2001:30::/64','2002:10::/64','2002:20::/64','2002:30::/64')
        i=0
        for ip in list_iproute:
            if ip  in return_ip_route:
                i+=1
                print(f"Ip route {ip} ok!",i)
            else:
                if ip  not in return_ip_route:
                    print(f"No ip route {ip} ")
        if i==6:
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
            print("Interface availeble, RIPng OK")
            return True
        else:
            print("Interface is not available, RIPng bad ")
            return False
    except ValueError as err:
        return False
    
if __name__ == "__main__":
    result = check_ping_interf('2.2.2.2')
    print(result)