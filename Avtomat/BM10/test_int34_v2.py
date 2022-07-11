import re
import yaml
import pexpect
from pprint import pprint
from show_int34_netmiko import *
from cfg_int34_BM10 import *
from ping import ping_ip_3G
from ping import *
import time

from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)
command_sh_net = "uci show network | grep 34G"
command_cfg_34G = [
    "uci set network.34G=interface",
    "uci set network.34G.proto='qmi'",
    "uci set network.34G.device='/dev/cdc-wdm0'",
    "uci set network.34G.apn='internet.tele2.ru'",
    "uci set network.34G.pdptype='ipv4'",
    "uci commit",
    "reboot"
    ]
ip_dest = "8.8.8.8"
promo= " -w 4"
word_ping="ping "
command_ping = (word_ping+ip_dest+promo)

try:

    with open("BM10_LTE.yaml")as f:
        device = yaml.safe_load(f)
        for dev in device:
            result_sh_34G =  send_show_command(dev, command_sh_net)
            print(result_sh_34G)
            if 'addr' in result_sh_34G:
                ping_ip_3G(dev, command_ping)
                print("END")

            else:
                cfg_wwan_BM10(dev,command_cfg_34G)

except (NetmikoAuthenticationException, NetmikoTimeoutException) as error:
        print("*"*5, "Error connection to:", device['host'], "*"*5)

