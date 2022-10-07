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
ДОДЕЛАТЬ!!! Добавить пинг
 Проверка, что роутер отвечает и STP работает
"""
def check_rootSTP(comm):
    with open("BM10_LTE.yaml")as f:
        temp = yaml.safe_load(f)
        for t in temp:
            device = dict(t)
            r1 = Router(**device)
    try:

        temp = r1.send_sh_command(device, comm)

        # match1 = re.search(r'bridge id\s+(\S+)', temp)
        # match2 = re.search(r'designated root\s+(\S+)',temp)
        # print(match1.group(1))
        # print(match2.group(1))
        if "with own address as source address" in temp:
            return True
        else:
            return False
    except ValueError as err:
        return False

# if __name__ == "__main__":
#     result = check_rootSTP("brctl showstp br-lan")
#     print(result)
