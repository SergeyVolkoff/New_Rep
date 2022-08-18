import re
import yaml
import netmiko
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)
from clss_Router import *
class Tests ():
    def test_int3G(self,device):
        command_sh_net = "uci show network | grep 34G"
        device = dict(Router.device)
        r1 = Router(**device)
        result_sh_34G = r1.send_sh_command(device, command_sh_net)
        print(result_sh_34G)
        if 'addr' in result_sh_34G:
            result_ping = r1.ping_ip(dev, r1.command_ping)
            print("Test 3G ok: \n", result_ping)
        elif 'No interface on router' in result_sh_34G:
            print("Test 3G fail\n")
        elif 'network.34G.device' in result_sh_34G:
            print("Test 3G fail\n", "bad cfg, maybe reboot?")
        return result_ping
if __name__ == "__main__":

    device = Router.device
    r1=Roter(**device)
    print(r1.test_int3G(device))