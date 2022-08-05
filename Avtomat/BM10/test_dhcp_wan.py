import re
import yaml
import pexpect
from pprint import pprint
from send_sh_comm import send_sh_comm
from cfg_int34_BM10 import *
from ping import ping_ip
from ping import *
import time

from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)

command_sh_wan = "ifconfig |grep -A 1 wan "
try:
    with open("BM10_LTE.yaml")as f:
        device = yaml.safe_load(f)
        for dev in device:
            result_sh_wan = send_sh_comm(dev, command_sh_wan)
            for sec in result_sh_wan:
                if "inet addr" in result_sh_wan:
                    result_ping = ping_ip(dev, command_ping)
                    print("Test wan ok - ", result_ping )
                    break
            else:
                print("Test fail, no inet addr\n", result_sh_wan)

except (NetmikoAuthenticationException, NetmikoTimeoutException) as error:
        print("*"*5, "Error connection to:", device['host'], "*"*5)


