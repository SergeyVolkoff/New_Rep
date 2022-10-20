import re
import time
import yaml
import netmiko
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)
from clss_Router import Router
"""
Проверка зоны firewall, настраиваем 4 порт как ван, открываем инпут в firewall,  пингуем с соседа
"""
def check_Fwall():
    with open("BM10_LTE.yaml")as f:
        temp = yaml.safe_load(f)
        for t in temp:
            device = dict(t)

            for val in device.values():
                if val =='192.168.1.1':
                    r1 = Router(**device)
                    device1 = device

                if val =='192.168.2.1':
                    r2 = Router(**device)
                    device2 = device

    try:
        time.sleep(0)
        temp = r1.send_sh_command(device,r1.commands_Fwall_cfg)        #отправляем конфиг фаервола
        temp2 = r2.ping_ip(device1,r2.command_ping)                 # проверяем доступность соседа
        if "destination  available " in temp:               #если отвечает, значит firewall зона настроена правильно.
            return True
        else:
            if " out of destination" in temp:            #если не отвечает - не правльно настроена зона firewall.
                return False
    except ValueError as err:
        return False

# if __name__ == "__main__":
#      result = check_Fwall("uci show")
#      print(result)