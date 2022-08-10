import yaml
from pprint import pprint
from send_sh_comm import send_sh_comm
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)
from netmiko import *


def cfg_pass (device, commands, log = True):
    if log:
        print(f"Connect to {device['host']}...")
    result = {}
    try:
        with ConnectHandler(**device) as ssh:
            print(device['host'], "connected")

            temp=ssh.send_command(command_string="passwd", expect_string="passwd",read_timeout=1)
            print("!", temp)

            temp1 = ssh.send_command(command_string="Qq123456", expect_string="New password:", read_timeout=3)
            print("@",temp1)

            temp2 = ssh.send_command(command_string="Qq123456", expect_string=":", read_timeout=3)
            print("#", temp2)

            #temp3 = ssh.send_command(command_string="12345678", expect_string=":")
            #print("$", temp3)


    except (NetmikoAuthenticationException, NetmikoTimeoutException) as error:
        print("*"*5, "Error connection to:", device['host'], "*"*5)
if __name__== "__main__":
    commands = "root22"
    with open("BM10_LTE.yaml") as f:
        device = yaml.safe_load(f)
        for dev in device:
                cfg_pass(dev, commands)
