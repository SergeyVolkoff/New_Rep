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
Из всего базового конфига проверяется только та команда, что вводится в test.py 
Чек заточен на проверку включен ли аппаратный ускоритель в файервол
"""
with open("BM10_LTE.yaml") as f:
    temp = yaml.safe_load(f)
    for t in temp:
        device = dict(t)
        r1 = Router(**device)
def check_sup_ASIC(comm):
    try:
        temp = r1.send_sh_command(device, comm)
        #print(temp)
        if "offloading_hw='1'" in temp:
            return True
    except ValueError as err:
        return False
def check_firewall(comm):
    try:
        temp = r1.send_sh_command(device,comm)
        if "forward='ACCEPT'" in temp:
            return True
    except ValueError as err:
        return False
def check_name_dev(comm):
    try:
        temp = r1.send_sh_command(device, comm)
        if "DUT_7621" in temp:
            return True


    except ValueError as err:
        return False
# if __name__ == "__main__":
#      result = check_base_cfg("uci show")
#      print(result)