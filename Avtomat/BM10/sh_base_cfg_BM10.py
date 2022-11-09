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
                sp_dev = []
                sp_lan =[]
                sp_wan = []

                sp_dev_v=[]
                sp_dev_v1=[]
                result = {}
                output = ssh.send_command(command).split('\n')
                # output = output.replace('=', '":"')
                # output = output.replace('\n', '","')
                # output = ('{"' + output + '"}')         # доводим внешний вид до словаря
                # result = json.loads(output)         # переделываем строку в словарь
                for line in output:
                    if 'network.wan.' in line:
                        interf = 'WAN'
                        data_interf = (line.split('=')[1])     # сплитуем значение после знака равно
                        sp_wan.append(data_interf)             # добавляем полученное значение в список
                        str_wan = " ".join(map(str, sp_wan))  # объединяем список строк в строку
                        result[interf] = str_wan +"\n"             # делаем словарь из ключа и значения в строке

                    """
                    Next: Firewall zone Wan and Lan
                    """
                    if 'firewall.@zone' in line:
                        if "[0]" in line:
                            interf = 'Firewall_zone_LAN'
                            if "input" in line:
                                str_fw = []
                                sp_fw = []
                                data_interf = (line.split('=')[1])     # сплитуем значение после знака равно
                                sp_fw.append(data_interf)             # добавляем полученное значение в список
                                str_fw = " ".join(map(str, sp_fw))  # объединяем список строк в строку
                                result[interf]= "LAN input" + str_fw +"\n"             # делаем словарь из ключа и значения в строке
                            if "output" in line:
                                data_interf = (line.split('=')[1])  # сплитуем значение после знака равно
                                str_fw = []
                                sp_fw = []
                                sp_fw.append(data_interf)  # добавляем полученное значение в список
                                str_fw = " ".join(map(str, sp_fw))  # объединяем список строк в строку
                                result[interf] += "LAN output" + str_fw +"\n" # делаем словарь из ключа и значения в строке
                            if "forward" in line:
                                data_interf = (line.split('=')[1])     # сплитуем значение после знака равно
                                str_fw = []
                                sp_fw = []
                                sp_fw.append(data_interf)             # добавляем полученное значение в список
                                str_fw = " ".join(map(str, sp_fw))  # объединяем список строк в строку
                                result[interf] += "LAN forward" + str_fw +"\n"            # делаем словарь из ключа и значения в строке
                    if 'firewall.@zone' in line:
                        if "[1]" in line:
                            interf = 'Firewall_zone_WAN'
                            if "input" in line:
                                data_interf = (line.split('=')[1])     # сплитуем значение после знака равно
                                str_fw = []
                                sp_fw = []
                                sp_fw.append(data_interf)             # добавляем полученное значение в список
                                str_fw = " ".join(map(str, sp_fw))  # объединяем список строк в строку
                                result[interf]= "WAN input" + str_fw+"\n"              # делаем словарь из ключа и значения в строке
                            if "output" in line:
                                data_interf = (line.split('=')[1])  # сплитуем значение после знака равно
                                str_fw = []
                                sp_fw = []
                                sp_fw.append(data_interf)  # добавляем полученное значение в список
                                str_fw = " ".join(map(str, sp_fw))  # объединяем список строк в строку
                                result[interf] += "WAN output" + str_fw +"\n"  # делаем словарь из ключа и значения в строке
                            if "forward" in line:
                                data_interf = (line.split('=')[1])     # сплитуем значение после знака равно
                                str_fw = []
                                sp_fw = []
                                sp_fw.append(data_interf)             # добавляем полученное значение в список
                                str_fw = " ".join(map(str, sp_fw))  # объединяем список строк в строку
                                result[interf] += "WAN forward" + str_fw +"\n"            # делаем словарь из ключа и значения в строке
                    """
                    END Firewall zone Wan and Lan
                    """

                    if 'network.lan.' in line:
                        interf = 'LAN'
                        data_interf = (line.split('=')[1])     # сплитуем значение после знака равно
                        sp_lan.append(data_interf)             # добавляем полученное значение в список
                        str_lan = " ".join(map(str, sp_lan))  # объединяем список строк в строку
                        result[interf] = str_lan              # делаем словарь из ключа и значения в строке

                    if 'network.@device[0].' in line:
                        interf = 'device'
                        data_interf = (line.split('=')[1])  # сплитуем значение после знака равно
                        sp_dev.append(data_interf)            # добавляем полученное значение в список
                        str_dev = " ".join(map(str,sp_dev))     # объединяем список строк в строку
                        result[interf]=str_dev+"\n"                # делаем словарь из ключа и значения в строке

                    if 'network.@bridge-vlan[0]' in line:
                        if 'network.@bridge-vlan[0].vlan'in line:
                            vlan_name = (line.split('=')[1])
                            interf = format(f"bridge_Vlan{vlan_name}")
                        data_interf = (line.split('=')[1])  # сплитуем значение после знака равно
                        sp_dev_v.append(data_interf)            # добавляем полученное значение в список
                        str_dev_v = " ".join(map(str,sp_dev_v))     # объединяем список строк в строку
                        result[interf]=str_dev_v +"\n"                # делаем словарь из ключа и значения в строке

                    if 'network.@bridge-vlan[1]' in line:
                        if 'network.@bridge-vlan[1].vlan'in line:
                            vlan_name = (line.split('=')[1])
                            interf = format(f"bridge_Vlan{vlan_name}")
                        data_interf = (line.split('=')[1])  # сплитуем значение после знака равно
                        sp_dev_v1.append(data_interf)            # добавляем полученное значение в список
                        str_dev_v1 = " ".join(map(str,sp_dev_v1))     # объединяем список строк в строку
                        result[interf]=str_dev_v1  +"\n"             # делаем словарь из ключа и значения в строке

        pprint(result)
        list_key = list(result.keys())
        all_key = " ".join(list_key)

        all_values = " ".join(list(result.values()))
       # print(all_values)

        c = Console()
        table = Table()

        for name,date in result.items():
            table.add_column(name)
        for name, date in result.items():
            table.add_row(date)


        c.print(table)


        # all_val = " ".join(list(result.values()))
        # for key in all_key.split():
        #     print(key)
        #     table.add_column(key)
        # for val in result.values():
        #     pass
        #     all_val = " ".join(list(val))
        #     print(all_val)
        #     table.add_row(all_val)

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
    "uci show",
    # "uci show network.lan",
    # "uci show network.@route[0]"
    ]
    with open("BM10_LTE.yaml")as f:
        device = yaml.safe_load(f)
        for dev in device:
            pprint(sh_base_cfg_BM10(dev, commands))
