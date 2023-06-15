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
Чек заточен на проверку включена ли аппаратная обрботка трафика, 
Включен ли файрвол на ван порту,
Проверка имени устр-ва,
Проверка времени устр-ва
Проверка NTP
Проверка имени вайфай
Проверка включен ли mwan3
"""
with open("BM10_LTE.yaml") as f:
    temp = yaml.safe_load(f)
    for t in temp:
        device = dict(t)
        r1 = Router(**device)
def check_sup_ASIC(comm): # Проверка включена ли аппаратная обрботка трафика
    try:
        temp = r1.send_sh_command(device, comm)
        #print(temp)
        if "offloading_hw='1'" in temp:
            return True
    except ValueError as err:
        return False
def check_firewall(comm): # Включен ли файрвол на ван порту
    try:
        temp = r1.send_sh_command(device,comm)
        if "forward='ACCEPT'" in temp:
            return True
    except ValueError as err:
        return False
def check_name_dev(comm): # Проверка имени устр-ва
    try:
        temp = r1.send_sh_command(device, comm)
        if "DUT_7621" in temp:
            return True
    except ValueError as err:
        return False

def check_ntp(comm):
    try:
        temp= r1.send_sh_command(device,comm)
        if "ntp-servers" in temp:
            return True
    except ValueError as err:
        return False
def check_time_zone (comm): # Проверка времени устр-ва
    try:
        temp= r1.send_sh_command(device,comm)
        if "Europe/Moscow" in temp:
            return True
    except ValueError as err:
        return False
def check_wifi_name(comm): # Проверка имени вайфай
    try:
        temp = r1.send_sh_command(device, comm)
        if "DUT_7621" in temp:
            return True
    except ValueError as err:
        return False

def check_mwan3(com):  # Проверка включен ли mwan3

        # temp=r1.send_sh_command(device,com)
        temp= re.search(r'0.0.0.0/0',r1.send_sh_command(device,com))
        if temp!=None:
            temp_reg = temp.group()
            print(temp_reg)
            return False
        else:
            print(temp)
            return True


if __name__ == "__main__":
     result = check_mwan3("mwan3 status")
     print(result)