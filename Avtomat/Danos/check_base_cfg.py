import re
import yaml
import netmiko
import paramiko
import time
from paramiko import SSHClient
from scp import SCPClient
from rich import print
from rich.theme import Theme
from rich.console import Console
from pprint import pprint
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException
)
from cls_Danos import Danos
from rich.theme import Theme

try:
    with open("BM1300_danos.yaml") as f1:
        temp = yaml.safe_load(f1)
        for t in temp:
            device = dict(t)
            dan = Danos(**device)
except(NetmikoAuthenticationException, NetmikoTimeoutException) as error:
            print("*" * 5, "Error connection to:", device['host'], "*" * 5)
def check_hostname(command):
    try:
        temp = dan.ssh.send_command(command)
        if "Aggregation-switch-DUT-Aggregation-switch-DUT-Aggregation-switc" in temp:
            print("Hostname OK")
            return True
        else:
            print("Bad name host")
            return False
    except ValueError as err:
        return False
def check_len_hostname(command):
    try:
        temp = dan.ssh.send_command(command)
        if len(temp) == 63:
            print("Lens Hostname 63 and OK")
            return True
        else:
            print("Bad lens Hostname")
            return False
    except ValueError as err:
        return False
def check_bad_len_host(command):
    try:
        cfg_bad_lens_name= dan.ssh.send_config_set("set system host-name A_")
        output_commit = dan.ssh.commit()
        output_discon = dan.ssh.disconnect()
        temp = dan.ssh.send_command("sh host name")
        if "AWER" in temp:
            print(" Hostname  OK")
            return True
        else:
            print("Bad  Hostname")
            return False
    except ValueError as err:
        return False
if __name__== "__main__":
    print(check_bad_len_host("sh host name"))
