import re
import yaml
import netmiko
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)
from clss_Router import Router
"""
 Проверка, что роутер рутовый в STP
"""
def check_rootSTP(comm):
    with open("~/Documents/new/New_Rep/Avtomat/BM10/BM10_LTE.yaml")as f:
        temp = yaml.safe_load(f)
        for t in temp:
            device = dict(t)
            r1 = Router(**device)
    try:
        temp = r1.send_sh_command(device, comm)

        match1 = re.search(r'bridge id\s+(\S+)', temp)
        match2 = re.search(r'designated root\s+(\S+)',temp)
        print(match1.group(1))
        print(match2.group(1))

        if match1.group(1) == match2.group(1):
            return True
        else:
            return False
    except ValueError as err:
        return False

if __name__ == "__main__":
    result = check_rootSTP("brctl showstp br-lan")
    print(result)