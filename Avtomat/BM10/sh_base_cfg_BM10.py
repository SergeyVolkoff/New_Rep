import re
import yaml
import netmiko
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)

def sh_base_cfg_BM10(device, commands,log = True):
    if log:
        print(f"Connect to {device['host']}...")

    try:
        with ConnectHandler(**device) as ssh:
            print(device['host'], "connected")
            for command in commands:
                output = ssh.send_command(command)
                if output:
                    print(output)


    except (NetmikoAuthenticationException, NetmikoTimeoutException) as error:
        print("*"*20, "ERROR", "*"*20)


if __name__ == "__main__":
    commands = ["uci show system.@system[0].hostname", "uci show system.ntp.server", "uci show firewall.@zone[1].forward"]
    with open("BM10_LTE.yaml")as f:
        device = yaml.safe_load(f)

        for dev in device:
            print(sh_base_cfg_BM10(dev, commands))
