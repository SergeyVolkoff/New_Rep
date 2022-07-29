import re
import yaml
import netmiko
from pprint import pprint
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)

def sh_base_cfg_BM10(device, commands,log = True):
    if log:
        print(f"Connect to {device['host']}...")

    try:
        result={}
        with ConnectHandler(**device) as ssh:
            print(device['host'], "connected")
            for command in commands:
                output = ssh.send_command(command)
                result[command] =  output
        return " ".join(list(result.values()))

    except (NetmikoAuthenticationException, NetmikoTimeoutException) as error:
        print("*"*5, "Error connection to:", device['host'], "*"*5)


if __name__ == "__main__":
    commands = [
    "uci show system.@system[0].hostname",
    "uci show firewall.@zone[1].input",
    "uci show firewall.@zone[1].output",
    "uci show firewall.@zone[1].forward",
    "uci show firewall.@defaults[0].flow_offloading",
    "uci show firewall.@defaults[0].flow_offloading_hw"
    "uci show wireless.default_radio0.ssid"
    "uci show network.wan",
    "uci show network.lan",
    "uci show network.@route[0]"
    ]
    with open("BM10_LTE.yaml")as f:
        device = yaml.safe_load(f)
        for dev in device:
            pprint(sh_base_cfg_BM10(dev, commands))
