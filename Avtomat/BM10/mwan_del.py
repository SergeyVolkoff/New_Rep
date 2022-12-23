import ast
import re
import yaml
import netmiko

from pprint import pprint
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)
from rich.table import Table
from rich.console import Console
from rich.theme import Theme
import json  # для преобразования строки в словарь


my_colors = Theme( #добавляет цветовую градацию для rich
    {
        "success":"bold green",
        "fail":"bold red",
        "warning":"bold yellow"
    }
)

console = Console(theme=my_colors)

def mwan_del(device, commands,log = True):
    if log:
        console.print(f"Connect to {device['host']}...", style="warning")
    try:
        with ConnectHandler(**device) as ssh:
            console.print(device['host'], "connected!", style='success')
            for command in commands:
                result = {}
                output = ssh.send_config_set(commands)

                if "tracking is active" in output:
                    #output = self.ssh.send_command(command="mwan3 stop")
                    print("mwan active!")
                    output = ssh.send_command(command_string="mwan3 stop", read_timeout=10)
                    result["mwan stop"]=output

                elif "Usage: uci [<options>] <command> [<arguments>]" in output:
                    output = "bad command"
                    result = output
                else:
                    result=output
                    print("not mwan")
        return result
    except (NetmikoAuthenticationException, NetmikoTimeoutException) as error:
        console.print("*"*5, "Error connection to:", device['host'], "*"*5,style='fail')
if __name__ == "__main__":
    commands = [
    "mwan3 status",
    ]
    with open("BM10_LTE.yaml")as f:
        device = yaml.safe_load(f)
        for dev in device:
            print(mwan_del(dev, commands))