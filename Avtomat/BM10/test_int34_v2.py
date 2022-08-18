import re
import yaml
import pexpect
from pprint import pprint
from show_int34_netmiko import *
from cfg_int34_BM10 import *
from ping import ping_ip
from ping import *
import time

from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)
command_sh_net = "uci show network | grep 34G"
try:
    with open("BM10_LTE.yaml")as f:
        device = yaml.safe_load(f)
        for dev in device:
            result_sh_34G =  send_show_command(dev, command_sh_net)
            print("*"*8,result_sh_34G)
            if 'addr' in result_sh_34G:
                result_ping = ping_ip(dev, command_ping)
                print("Test 3G ok: \n",result_ping)
            elif 'No interface on router'in result_sh_34G:
                result_cfg = cfg_wwan_BM10(dev,command_cfg_34G)
                print("Test 3G fail\n", result_cfg)
            elif 'network.34G.device'in result_sh_34G:
                print("Test 3G fail\n", "bad cfg, maybe reboot?")

except (NetmikoAuthenticationException, NetmikoTimeoutException) as error:
        print("*"*5, "Error connection to:", device['host'], "*"*5)


