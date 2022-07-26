import re
import yaml
import netmiko
import sys
import textfsm
from sh_base_cfg_BM10 import sh_base_cfg_BM10

from pprint import pprint
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)

def  parse_command_output(template, command_output):
    with open(template) as tmpl:
        fsm = textfsm.TextFSM(tmpl)
        result = fsm.ParseText(command_output )
    return  result

commands = [
    "uci show system.@system[0].hostname",
    "uci show system.ntp.server",
    "uci show firewall.@zone[1].input",
    "uci show firewall.@zone[1].output",
    "uci show network.wan",
    "uci show network.lan",
    "uci show network.@route[0]"
    ]

if __name__ == "__main__":
    dev = {
         "device_type": "linux",
         "host": "192.168.1.1",
         "username": "root",
         "password": "root",
         "timeout": "1"
        }

    output = sh_base_cfg_BM10(dev, commands)
    with open ("data_file/sh_network.txt") as sh:
        print(output)
        result = parse_command_output("templates/sh_netw.template",output)
        print(result)

