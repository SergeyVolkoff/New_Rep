import yaml
import netmiko
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)
from clss_Router import Router
"""
  Из конфига вланов проверяем наличие вланов 2 и 3
"""
def check_vln_cfg(comm):
    with open ("BM10_LTE.yaml") as f:
        temp = yaml.safe_load(f)
        for t in temp:
            device = dict(t)
            r1 =Router(**device)
    try:
        temp = r1.send_sh_command(device,comm)
        if "bridge-vlan[1].ports='lan2'" in temp:
            return True

        if "bridge-vlan[2].ports='lan3'" in temp:
            return True
        else:
            return False
    except ValueError as err:
        return False
if __name__ == "__main__":
     result = check_vln_cfg("uci show network")
     print(result)