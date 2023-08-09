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
def check_ok_hostname(comm):
    try:
        ok_lens_name = dan.ssh.send_config_set(comm)
        output_commit = dan.ssh.commit()
        #output_discon = dan.ssh.disconnect()
        temp = dan.ssh.send_command("sh host name")
        if "Node exists" in ok_lens_name:
            print("this hostname is exist")
            return False
        elif "Set failed" in ok_lens_name:
            print("hostname is not valid")
            return False

        else:
            print("Hostname OK")
            return True
    except ValueError as err:
        return False

# def check_long_hostname(comm):
#     try:
#         long_name = dan.ssh.send_config_set(comm)
#         if " is not valid" not in long_name:
#             print("Hostname OK")
#             return True
#         else:
#             print("Bad name host")
#             return False
#     except ValueError as err:
#         return False
# def check_hostname():
#     try:
#         short_name= dan.ssh.send_config_set("set system host-name A_")
#         output_commit = dan.ssh.commit()
#         output_discon = dan.ssh.disconnect()
#         temp = dan.ssh.send_command("sh host name")
#         print (temp)
#         if " is not valid" not in short_name:
#             print("Hostname OK")
#             return True
#         else:
#             print("Bad name host")
#             return False
#     except ValueError as err:
#         return False
if __name__== "__main__":
    comm = "set system host-name Aggre"
    print(check_ok_hostname(comm))
