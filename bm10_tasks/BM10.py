# -*- coding: utf-8 -*-
import re
import yaml
import netmiko
import paramiko
import time
from rich import print
from rich.theme import Theme
from rich.console import Console
from pprint import pprint
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException
)
from rich.table import Table
#from netmiko.linux.linux_ssh import LinuxSSH
my_colors = Theme( #добавляет цветовую градацию для rich
    {
        "success":"bold green",
        "fail":"bold red",
        "warning":"bold yellow"
    }
)
console = Console(theme=my_colors)



class BM10():
    def __init__(self, device_type, host, username, timeout, password,**kwargs):
        try:
            with open("src/BM10_LTE.yaml") as f2:
                temp = yaml.safe_load(f2)
                for t in temp:
                    device = dict(t)

            self.ssh = ConnectHandler(**device)
            self.ip = host
            self.name = username
            self.passwd = password
            self.promo = " -w 4"
            self.word_ping = "ping "
            self.command_ping = self.word_ping+self.promo
        except(NetmikoAuthenticationException,NetmikoTimeoutException) as error:
            print("*" * 5, "Error connection to:", device['host'], "*" * 5)


    def check_connection(self,device,log=True):

        """
        ФУНКЦИЯ проверки установки соединения с роутером
        """

        if log:
            console.print(f"Connect to {device['host']}...", style="warning")
        try:
            with ConnectHandler(**device) as ssh:
                console.print(device['host'], "connected!", style='success')
        except (NetmikoAuthenticationException, NetmikoTimeoutException) as error:
            console.print("*" * 5, "Error connection to:", device['host'], "*" * 5, style='fail')


    def send_sh_command(self, device, command):

        """ФУНКЦИЯ отправки простой команды в уст-во по ssh, без импорта"""

        self.check_connection(device)         # вызов функции проверки соединения с роутером
        temp = self.ssh.send_command(command)
        result = temp
        return result
if __name__ == "__main__":
    with open("src/BM10_LTE.yaml")as f:
         temp = yaml.safe_load(f)
         for t in temp:
            device = dict(t)
            r1 = BM10(**device)
            print(r1.send_sh_command(device, "uci show"))