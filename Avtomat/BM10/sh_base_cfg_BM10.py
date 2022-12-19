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
        console.print(f"Connect to {device['host']}...",style = "warning")

    try:

        with ConnectHandler(**device) as ssh:
            console.print(device['host'], "connected!",style='success')
            for command in commands:
                if command == "route":
                    output = ssh.send_command(command)
                    console.print(output, style='success')
                else:
                    sp_dev = []
                    sp_lan =[]
                    sp_wan = []
                    sp_lte = []
                    sp_dev_v=[]
                    sp_dev_v1=[]
                    sp_wire = []
                    sp_hn = []
                    result = {}
                    output = ssh.send_command(command).split('\n')
                    # output = output.replace('=', '":"')
                    # output = output.replace('\n', '","')
                    # output = ('{"' + output + '"}')         # доводим внешний вид до словаря
                    # result = json.loads(output)         # переделываем строку в словарь
                    for line in output:
                        # 1.Hostname
                        if '.hostname' in line:
                            interf = 'Host \nname'
                            data_interf = (line.split('=')[1])     # сплитуем значение после знака равно
                            sp_hn.append(data_interf)             # добавляем полученное значение в список
                            str_hn = " ".join(map(str, sp_hn))  # объединяем список строк в строку
                            result[interf] = str_hn +"\n"             # делаем словарь из ключа и значения в строке
                            if 'BWOS' in data_interf:
                                console.print("No base cfg!", style='fail')
                        # 2.LTE status
                        if 'network.LTE.' in line:
                            interf = 'LTE'
                            data_interf = (line.split('=')[1])     # сплитуем значение после знака равно
                            sp_lte.append(data_interf)             # добавляем полученное значение в список
                            str_lte = " ".join(map(str, sp_lte))  # объединяем список строк в строку
                            result[interf] = str_lte +"\n"             # делаем словарь из ключа и значения в строке
                        # 3.WAN
                        if 'network.wan.' in line:
                            interf = 'WAN'
                            data_interf = (line.split('=')[1])     # сплитуем значение после знака равно
                            sp_wan.append(data_interf)             # добавляем полученное значение в список
                            str_wan = " ".join(map(str, sp_wan))  # объединяем список строк в строку
                            result[interf] = str_wan +"\n"             # делаем словарь из ключа и значения в строке
                        # 4.WIFI
                        if 'wireless.default_radio' in line:
                            if "ssid" in line:
                                interf = 'Wireless'
                                data_interf = (line.split('=')[1])  # сплитуем значение после знака равно
                                sp_wire.append(data_interf)  # добавляем полученное значение в список
                                str_wire = " ".join(map(str, sp_wire))  # объединяем список строк в строку
                                result[interf] = str_wire + "\n"  # делаем словарь из ключа и значения в строке

                        # 5,6. Next: Firewall zone Wan and Lan

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
                                    str_fw = []
                                    sp_fw = []
                                    data_interf = (line.split('=')[1])  # сплитуем значение после знака равно
                                    sp_fw.append(data_interf)  # добавляем полученное значение в список
                                    str_fw = " ".join(map(str, sp_fw))  # объединяем список строк в строку
                                    result[interf] = "LAN output" + str_fw +"\n" # делаем словарь из ключа и значения в строке
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
                                    result[interf] = "WAN output" + str_fw +"\n"  # делаем словарь из ключа и значения в строке
                                if "forward" in line:
                                    data_interf = (line.split('=')[1])     # сплитуем значение после знака равно
                                    str_fw = []
                                    sp_fw = []
                                    sp_fw.append(data_interf)             # добавляем полученное значение в список
                                    str_fw = " ".join(map(str, sp_fw))  # объединяем список строк в строку
                                    result[interf] += "WAN forward" + str_fw +"\n"            # делаем словарь из ключа и значения в строке
                        # 7.LAN
                        if 'network.lan.' in line:
                            interf = 'LAN'
                            data_interf = (line.split('=')[1])     # сплитуем значение после знака равно
                            sp_lan.append(data_interf)             # добавляем полученное значение в список
                            str_lan = " ".join(map(str, sp_lan))  # объединяем список строк в строку
                            result[interf] = str_lan +"\n"             # делаем словарь из ключа и значения в строке
                        # 8. Device
                        if 'network.@device[0].' in line:
                            interf = 'device'
                            data_interf = (line.split('=')[1])  # сплитуем значение после знака равно
                            sp_dev.append(data_interf)            # добавляем полученное значение в список
                            str_dev = " ".join(map(str,sp_dev))     # объединяем список строк в строку
                            result[interf]=str_dev+"\n"                # делаем словарь из ключа и значения в строке
                        # 9. Bridge-vlan
                        if 'network.@bridge-vlan[0]' in line:
                            if 'network.@bridge-vlan[0].vlan'in line:
                                vlan_name = (line.split('=')[1])
                                interf = format(f"bridge_Vlan{vlan_name}")
                            data_interf = (line.split('=')[1])  # сплитуем значение после знака равно
                            sp_dev_v.append(data_interf)            # добавляем полученное значение в список
                            str_dev_v = " ".join(map(str,sp_dev_v))     # объединяем список строк в строку
                            result[interf]=str_dev_v +"\n"                # делаем словарь из ключа и значения в строке
                        # 10. Bridge 2
                        if 'network.@bridge-vlan[1]' in line:
                            if 'network.@bridge-vlan[1].vlan'in line:
                                vlan_name = (line.split('=')[1])
                                interf = format(f"bridge_Vlan{vlan_name}")
                            data_interf = (line.split('=')[1])  # сплитуем значение после знака равно
                            sp_dev_v1.append(data_interf)            # добавляем полученное значение в список
                            str_dev_v1 = " ".join(map(str,sp_dev_v1))     # объединяем список строк в строку
                            result[interf]=str_dev_v1  +"\n"             # делаем словарь из ключа и значения в строке
            if command == "route":
                output = ssh.send_command(command)
                #console.print(output, style='success')
        list_value = list(result.values())
        str_value = ', '.join(list_value)

        c = Console()
        table = Table()
        for name,date in result.items():
            table.add_column(name)
        col_val = len(list_value)
        table.add_row(
            list_value[0], list_value[1],list_value[2],
            list_value[3],list_value[4],list_value[5],
            list_value[6]
        )
        c.print(table )
    except (NetmikoAuthenticationException, NetmikoTimeoutException) as error:
        console.print("*"*5, "Error connection to:", device['host'], "*"*5,style='fail')

if __name__ == "__main__":
    commands = [
    "uci show",
    "route"
    ]
    with open("BM10_LTE.yaml")as f:
        device = yaml.safe_load(f)
        for dev in device:
            print(sh_base_cfg_BM10(dev, commands))
