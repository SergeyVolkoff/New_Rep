import re
import yaml
import netmiko
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)
from clss_Router import Router

with open("BM10_LTE.yaml") as f:
    temp = yaml.safe_load(f)
    for t in temp:
        device = dict(t)
        r1 = Router(**device)
def check_WiFi_AP(comm):
    try:
        temp = r1.send_sh_command(device, comm)
        if "Br_AP" in temp:
            return True
        else:
            return False
    except ValueError as err:
        return False
def check_pingGW(comm):
    try:
        temp2 = r1.ping_ip(device,r1.command_ping)              # проверяем доступность соседа
        if "destination  available " in temp2:               #если отвечает, значит firewall зона настроена правильно.
            return True
        else:
            if " out of destination" in temp2:            #если не отвечает - не правльно настроена зона firewall.
                return False
    except ValueError as err:
        return False
if __name__ =="__main__":
    result = check_WiFi_AP( "uci show network")
    print (result)
