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
def check_base_cfg(comm):
    with open("BM10_LTE.yaml")as f:
        temp = yaml.safe_load(f)
        for t in temp:
            device = dict(t)
            r1 = Router(**device)
    try:
        temp = r1.send_sh_command(device, comm)
        if "offloading_hw='1'" in temp:
            return True
        if "forward='ACCEPT'" in temp:
            return  True
    except ValueError as err:
        return False