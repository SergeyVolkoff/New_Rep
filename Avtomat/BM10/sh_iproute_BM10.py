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

my_colors = Theme( #добавляет цветовую градацию для rich
    {
        "success":"bold green",
        "fail":"bold red",
        "warning":"bold yellow"
    }
)
console = Console(theme=my_colors)


def sh_iproute_BM10(device, commands,log = True):
    if log:
        console.print(f"Connect to {device['host']}...",style = "warning")
    try:
        with ConnectHandler(**device) as ssh:
            console.print(device['host'], "connected!",style='success')
            for command in commands:
                if command == "route":
                    output = ssh.send_command(command)
                    console.print(output, style='success')
                else:
                    break

    except (NetmikoAuthenticationException, NetmikoTimeoutException) as error:
        console.print("*"*5, "Error connection to:", device['host'], "*"*5,style='fail')

if __name__ == "__main__":
    commands = [
    "route",
    "show network"
    ]
    with open("BM10_LTE.yaml")as f:
        device = yaml.safe_load(f)
        for dev in device:
            pprint(sh_iproute_BM10(dev, commands))