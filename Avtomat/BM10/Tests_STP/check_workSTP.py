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
 
 Проверка, что соседний роутер отвечает и STP работает,  что есть порт только в прослушивании!
"""
def check_workSTP(comm):
    with open("~/Documents/new/New_Rep/Avtomat/BM10/BM10_LTE.yaml")as f:
        temp = yaml.safe_load(f)
        for t in temp:
            device = dict(t)
            r1 = Router(**device)
            print(r1)

    try:

        r1.send_sh_command(device, "/etc/init.d/log restart")  # очищаем логи
        print("log clear!input cable")
        print(" Для проверки нужно кольцо или избыточный линк на 3 и 4 портах, ждем 10 сек")
        time.sleep(12)
        temp = r1.send_sh_command(device, comm)                      #вызываем логи
        if "port 4(lan4) entered blocking state" in temp:           #если порт в блоке, значит STP работает.
            return True
        else:
            if " port 4(lan4) entered forwarding state" in temp:  #если порт перешел в форвард - STP не работает.
                return False
    except ValueError as err:
        return False

if __name__ == "__main__":
     result = check_workSTP("logread -l 10")
     print(result)
