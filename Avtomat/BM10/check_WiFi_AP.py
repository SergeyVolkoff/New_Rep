import re
import yaml
import netmiko
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)
from clss_Router import Router
def check_WiFi_AP(comm):
    with open("BM10_LTE.yaml")as f:
        temp = yaml.safe_load(f)
        for t in temp:
            device = dict(t)
            r1 = Router(**device)
    try:
        temp = r1.send_sh_command(device, comm)
        if "Br_AP" in temp:
            return True
        else:
            return False
    except ValueError as err:
        return False

if __name__ =="__main__":
    result = check_WiFi_AP( "uci show network")
    print (result)
