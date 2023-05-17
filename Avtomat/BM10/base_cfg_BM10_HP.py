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



if __name__ == "__main__":
    # file_cfg = "dut_r1.txt"
    # with open (file_cfg) as f:
    #     commands = [f.read()]
    commands = [

    "uci set system.@system[0].hostname='DUT_7621_rc1.2'",
    "uci set system.ntp.server='ntp0.ntp-servers.net'",
    "uci set system.@system[0].zonename='Europe/Minsk'",
    "uci set system.@system[0].timezone='<+03>-3'",
    "uci set firewall.@zone[1].forward='ACCEPT'",
    "uci set firewall.@zone[1].input='ACCEPT'",

    "uci set firewall.@defaults[0].input='ACCEPT'",
    "uci set firewall.@defaults[0].output='ACCEPT'",
    "uci set firewall.@defaults[0].flow_offloading='1'",
    "uci set firewall.@defaults[0].flow_offloading_hw='1'",
    "uci set firewall.@defaults[0].synflood_protect='1'",
    "uci set firewall.@defaults[0].forward='ACCEPT'",
    "uci set firewall.@defaults[0].flow_offloading='1'",
    "uci set firewall.@defaults[0].flow_offloading_hw='1'",

    "uci set network.wan.proto='static'",
    "uci set network.wan.ipaddr='200.1.1.1'",
    "uci set network.wan.netmask='255.255.255.0'",

    "uci set wireless.default_radio0.ssid='DUT7621_RC1.2'",
    "uci set wireless.default_radio0.encryption='psk2'" ,
    "uci set wireless.default_radio0.key='12345678'" ,
    "uci set wireless.radio0.disabled=0",
    "uci commit",
    "mwan3 stop"

    ]

    with open("BM10_LTE.yaml") as f:
        device = yaml.safe_load(f)
        for dev in device:
            pprint(base_cfg(dev, commands))








