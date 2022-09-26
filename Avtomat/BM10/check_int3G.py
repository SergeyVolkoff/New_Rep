import re
import yaml
import netmiko
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)
from clss_Router import Router

def check_int3G(comm):
    with open("BM10_LTE.yaml")as f:
        temp = yaml.safe_load(f)
        for t in temp:
            device = dict(t)
            r1 = Router(**device)
    try:
        temp = r1.show_int3G(device,comm)
        if "network.34G.device" in temp:
            return True
        if "No interface on router" in temp:
            return False
    except ValueError as err:
        return False
if __name__ =="__main__":
    result = check_int3G("uci show network | grep 34G")
    print (result)
