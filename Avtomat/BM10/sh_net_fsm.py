import re
import yaml
import netmiko
import sys
import textfsm
from sh_base_cfg_BM10 import sh_base_cfg_BM10
from tabulate import tabulate
from pprint import pprint
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)

def  parse_command_output(template, command_output):
    with open(template) as tmpl:
        fsm = textfsm.TextFSM(tmpl)
        header = fsm.header
        result = fsm.ParseText(command_output )
        print(tabulate(result, headers=header))
commands = [
   "uci show"
    ]

if __name__ == "__main__":
    with open("BM10_LTE.yaml") as f:
        device = yaml.safe_load(f)
        for dev in device:
            output = sh_base_cfg_BM10(dev, commands)
            print(output)
            with open ("data_file/sh_network.txt") as sh:
                result = parse_command_output("templates/sh_netw.template",output)


