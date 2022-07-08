import re
import pexpect
from pprint import pprint
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)
import yaml

def cfg_wwan_BM10(device,commands):
    result=""
    try:
        with ConnectHandler(**device) as ssh:
            print(device['host'], "connected")
            for command in commands:
                output = ssh.send_command(command)
                print(command, ": in progress")
        return  result
    except (NetmikoAuthenticationException, NetmikoTimeoutException) as error:
        print("*"*20, "ERROR", "*"*20)

if __name__ == "__main__":
    commands = [
    "uci set network.34G=interface",
    "uci set network.34G.proto='qmi'",
    "uci set network.34G.device='/dev/cdc-wdm0'",
    "uci set network.34G.apn='internet.tele2.ru'",
    "uci set network.34G.pdptype='ipv4'",
    "uci commit",
    "reboot"
    ]
    with open("BM10_LTE.yaml")as f:
        device = yaml.safe_load(f)
        for dev in device:
            print(cfg_wwan_BM10(dev, commands))


