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
from rich.theme import Theme

my_colors = Theme( #добавляет цветовую градацию для rich
    {
        "success":"bold green",
        "fail":"bold red",
        "warning":"bold yellow"
    }
)
console = Console(theme=my_colors)
class Danos():
    def __init__(self,device_type, host, username, password,timeout, **kwargs):
        try:
            with open("BM1300_danos.yaml") as f1:
                temp = yaml.safe_load(f1)
                for t in temp:
                    device = dict(t)


            self.ssh = ConnectHandler(**device)
            self.ip = host
            self.name = username
            self.passwd = password
            self.promo = " -w 4"
            self.word_ping = "ping "
            self.command_ping = self.word_ping + self.promo
            self.ip_for_ping = '200.1.1.1'

            with open("commands_base_cfg.yaml") as f2:  # команды сброса конфига
                self.commands_base_cfg = yaml.safe_load(f2)

        except(NetmikoAuthenticationException, NetmikoTimeoutException) as error:
            print("*" * 5, "Error connection to:", device['host'], "*" * 5)

    """
    ФУНКЦИЯ настройки базового конфига
    """
    def base_cfg(self, commands_base_cfg):
        result = {}
        for command in self.commands_base_cfg:
            # output = self.ssh.send_command(command, expect_string=":", read_timeout=1)
            # print(output)
            output_cfg = self.ssh.send_config_set(command,exit_config_mode=False)
            output_commit = self.ssh.commit()
            if "Node exists" in output_cfg:
                console.print(command, " - Node exists!!!", style="success")
            if "Value validation failed" in result:
                console.print(command, " - Set failed", style='fail')

        output_sh_inf=self.ssh.send_command("run show interf")
        print(output_sh_inf)
        return output_cfg
if __name__ == "__main__":
    with open("BM1300_danos.yaml")as f:
         temp = yaml.safe_load(f)
         for t in temp:
            device = dict(t)
            dan = Danos(**device)
            dan.base_cfg(dan.commands_base_cfg)


