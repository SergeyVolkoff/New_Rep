import re
import yaml
import netmiko
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)
from clss_Router import Router

'''
Проверяем работу роутера как РРРоЕ клиента:

'''
with open("BM10_LTE.yaml") as f:
    temp = yaml.safe_load(f)
    for t in temp:
        device = dict(t)
        r1 = Router(**device)

def check_int_pppoe_cl(comm):        # Определяем наличие настроенного интерфейса ван с РРРоЕ (есть ли конфиг вообще)
    try:
        temp = r1.send_sh_command(device, comm)
        if "PPPoE" in temp:
            return True
        else:
            return False
    except ValueError as err:
        return False
def check_ping_inet():
    r1.ip_for_ping = "8.8.8.8"

    try:
        res_ping_inet = r1.ping_ip(device,r1.command_ping)
        if "destination  available" in res_ping_inet:
            print("PPPoE OK")
        else:
            print("PPPoE bad, inet(8.8.8.8)- not available")
    except ValueError as err:
        return False

if __name__ =="__main__":
    result = check_ping_inet()
    print (result)

