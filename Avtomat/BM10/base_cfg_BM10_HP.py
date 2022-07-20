'''
Base cfg host name, time serv, firewall, Hardware flow
'''


import re
import yaml
import netmiko
from jinja2 import Environment, FileSystemLoader
from gener_base_templ_cfg_BM10 import generate_config
from pprint import pprint
from sh_base_cfg_BM10 import sh_base_cfg_BM10
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)

def base_cfg(device, commands,log = True):
    if log:
        print(f"Connect to {device['host']}...")
    result = {}
    try:
        with ConnectHandler(**device) as ssh:
            print(device['host'], "connected")
            for command in commands:
                output = ssh.send_command(command, expect_string="",read_timeout=1)
                if "" in output:
                    output = "command passed"
                    result[command] = output

                elif "Usage: uci [<options>] <command> [<arguments>]" in output:
                    output = "bad command"
                    result[command] = output
        return result

    except (NetmikoAuthenticationException, NetmikoTimeoutException) as error:
        print("*"*5, "Error connection to:", device['host'], "*"*5)


if __name__ == "__main__":
    file_cfg = "dut_r1.txt"
    with open (file_cfg) as f:
        commands = [f.read()]
    # commands = [
    # "uci set system.@system[0].hostname='DUT'",
    # "uci set system.ntp.server='0.ntp2.stratum2.ru'",
    # "uci set firewall.@zone[1].forward='ACCEPT'",
    # "uci set firewall.@zone[1].input='ACCEPT'",
    # "uci set firewall.@defaults[0].flow_offloading='1'",
    # "uci set firewall.@defaults[0].flow_offloading_hw='1'",
    # "uci set network.lan.ipaddr='192.168.2.1'",
    # "uci set network.wan.proto='static'",
    # "uci set network.wan.ipaddr='200.1.1.1'",
    # "uci set network.wan.netmask='255.255.255.0'",
    # "uci commit"
    # ]

    print (commands)
    with open("BM10_LTE.yaml") as f:
        device = yaml.safe_load(f)
        for dev in device:
            pprint(base_cfg(dev, commands))








