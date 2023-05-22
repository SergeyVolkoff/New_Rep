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
Проверяем работу моста поднятого с телефоном
'''

with open("BM10_LTE.yaml") as f:
    temp = yaml.safe_load(f)
    for t in temp:
        device = dict(t)
        r1 = Router(**device,ip_for_ping=1)
# def check_WiFi_AP(comm):        # Определяем наличие настроенного бриджа (есть ли конфиг)
#     try:
#         temp = r1.send_sh_command(device, comm)
#         if "Br_AP" in temp:
#             return True
#         else:
#             return False
#     except ValueError as err:
#         return False
def check_pingGW():     # Пингуем шлюз-телефон
    output_rout = r1.send_sh_command(device,"ip route")
    ip_route = re.search(r'default via (\S+)',output_rout).group()
    print(output_rout)
    print(ip_route)
    r1.ip_dest=ip_route
    print(r1.ip_dest)

    try:
        temp2 = r1.ping_ip(device,r1.command_ping)              # проверяем доступность соседа
        if "destination  available " in temp2:               #если отвечает, значит
            return True
        else:
            if " out of destination" in temp2:            #если не отвечает - не правльно настроена
                return False
    except ValueError as err:
        return False

if __name__ =="__main__":
    result = check_pingGW()
    print (result)
