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
Проверяется выдан ли адрес на 3G интерфейсе, использует импортированую
ф-ю show_int3G из класса Router. Сверяет вывод из результата этой ф-ии.
"""
def check_int3G(comm):
    with open("BM10_LTE.yaml")as f:
        temp = yaml.safe_load(f)
        for t in temp:
            device = dict(t)
            r1 = Router(**device)
    try:
        temp = r1.show_int3G(device,comm)
        if "addr" in temp:
            return True
        if " but d'nt have ip addr" in temp:
             return True
        else:
            return False
    except ValueError as err:
        return False
# if __name__ =="__main__":
#     result = check_int3G("uci show network | grep 34G")
#     print (result)
