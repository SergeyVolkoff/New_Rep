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
def sh_base_cfg_BM10(device, commands,log = True):
    if log:
        print(f"Connect to {device['host']}...")

    try:

        with ConnectHandler(**device) as ssh:
            console.print(device['host'], "connected",style='success')
            for command in commands:
                result = {}
                output = ssh.send_command(command)
                output = output.replace('=', '":"')
                output = output.replace('\n', '","')
                output = ('{"' + output + '"}')         # доводим внешний вид до словаря
                result = json.loads(output)         # переделываем строку в словарь

        if "wan" in result:

        c = Console()
        table = Table(show_lines=True)
        for r in "command output".split():
            table.add_column(r)

        for comm, output in result.items():
            table.add_row(comm,output)
        c.print(table)


    except (NetmikoAuthenticationException, NetmikoTimeoutException) as error:
        console.print("*"*5, "Error connection to:", device['host'], "*"*5,style='fail')


if __name__ == "__main__":
    commands = [
    # "uci show system.@system[0].hostname",
    # "uci show firewall.@zone[1].input",
    # "uci show firewall.@zone[1].output",
    # "uci show firewall.@zone[1].forward",
    # "uci show firewall.@defaults[0].flow_offloading",
    # "uci show firewall.@defaults[0].flow_offloading_hw",
    # "uci show wireless.default_radio0.ssid",
    "uci show network.wan",
    # "uci show network.lan",
    # "uci show network.@route[0]"
    ]
    with open("BM10_LTE.yaml")as f:
        device = yaml.safe_load(f)
        for dev in device:
            pprint(sh_base_cfg_BM10(dev, commands))
