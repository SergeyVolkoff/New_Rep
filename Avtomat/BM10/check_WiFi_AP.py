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
Проверяем работу wifi моста поднятого с телефоном или роутером
'''

with open("BM10_LTE.yaml") as f:
    temp = yaml.safe_load(f)
    for t in temp:
        device = dict(t)
        r1 = Router(**device)
def check_WiFi_AP(comm):        # Определяем наличие настроенного бриджа (есть ли конфиг вообще нужный интерфейс)
    try:
        temp = r1.send_sh_command(device, comm)
        if "Br_AP" in temp:
            return True
        else:
            return False
    except ValueError as err:
        return False
def check_ping_inet():
    r1.ip_for_ping = "8.8.8.8"

    try:
        res_ping_inet = r1.ping_ip(device,r1.command_ping)
        if "destination available" in res_ping_inet:
            print("Bridge OK")
        else:
            print("Bridge bad, inet(8.8.8.8)- not available")
    except ValueError as err:
        return False
def check_pingGW():     # Пингуем шлюз-телефон
    output_rout = r1.send_sh_command(device,"ip route")              # этой командой получаем основной маршрут
    ip_route = re.search(r'default via (\S+)',output_rout).group(1)  # реджектим ip шлюза
    r1.ip_for_ping=ip_route                                          # переопределяем ip из основного класса R1

    try:
        res_pingGW = r1.ping_ip(device,r1.command_ping)           # проверяем доступность шлюза (
        if "destination  available " in res_pingGW:               #если отвечает, значит все ок, возвращаем тру
            print("GW available!")
            return True

        else:
            if " out of destination" in res_pingGW:            #если не отвечает - не правльно настроено, возвращаем фолс
                print("GW out")
                return False
    except ValueError as err:
        return False



if __name__ =="__main__":
    result = check_ping_inet()
    print (result)
