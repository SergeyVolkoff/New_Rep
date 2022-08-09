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
            for comm in commands:
                temp = ssh.send_command(command_string="passwd",expect_string= "New password:")
                print("!", temp)
                prompt = ssh.find_prompt()
                temp1=ssh.send_command(comm,expect_string=prompt)
                print("@", temp1)
                prompt = ssh.find_prompt()
                temp2 = ssh.send_command(comm, expect_string=prompt)
                print("#", temp2)
                prompt = ssh.find_prompt()
                temp3 = ssh.send_command(comm, expect_string=prompt)
                print("$", temp3)
            result = temp
        return result
    except (NetmikoAuthenticationException, NetmikoTimeoutException) as error:
        print("*"*5, "Error connection to:", device['host'], "*"*5)
if __name__== "__main__":
    commands = ["root12","root12","root12"]
    with open("BM10_LTE.yaml") as f:
        device = yaml.safe_load(f)
        for dev in device:
                cfg_pass(dev, commands)
