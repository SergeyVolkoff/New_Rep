import re
import pexpect
from pprint import pprint
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)
import yaml

command_cfg_34G = [
"uci set network.34G=interface",
"uci set network.34G.proto='qmi'",
"uci set network.34G.device='/dev/cdc-wdm0'",
"uci set network.34G.apn='internet.tele2.ru'",
"uci set network.34G.pdptype='ipv4'",
"uci commit",
"reboot"
]

def cfg_wwan_BM10(device,command_cfg_34G):
    result=""
    try:
        with ConnectHandler(**device) as ssh:
            print(device['host'], "connected for cfg")
            for command in command_cfg_34G:
                output = ssh.send_command(command)
                print(command, ": in progress")
        return  result
    except (NetmikoAuthenticationException, NetmikoTimeoutException) as error:
        print("*"*5, "Error connection to:", device['host'], "*"*5)

if __name__ == "__main__":

    with open("BM10_LTE.yaml")as f:
        device = yaml.safe_load(f)
        for dev in device:
            print(cfg_wwan_BM10(dev, command_cfg_34G))


