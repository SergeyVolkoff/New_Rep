# -*- coding: utf-8 -*-
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
from rich.console import Console
from rich.table import Table
from netmiko.linux.linux_ssh import LinuxSSH
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

class Router():
    def __init__(self, device_type, host, username, timeout, password,**kwargs):
        try:
            with open("BM10_LTE.yaml") as f2:
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


            with open ("commands_reset_cfg.yaml") as f1:            # команды сброса конфига
                self.commands_to_reset_conf = yaml.safe_load(f1)
            with open("commands_cfg_3G.yaml") as f:                 # команды настройки 3G
                self.commands_cfg_3G = yaml.safe_load(f)
            with open ("commands_base_cfg.yaml") as f3:             # команды настройки базового конфига(хост,firewall,wifi)
                self.commands_base_cfg = yaml.safe_load(f3)
            with open ("commands_802_1d_cfg.yaml") as f4:           # команды настройки STP+ базовые настройки
                self.commands_802_1d_cfg = yaml.safe_load(f4)
            with open ("commands_gre_config.yaml") as f5:           # команды настройки GRE-tun + базовые настройки
                self.commands_gre_config = yaml.safe_load(f5)
            with open("commands_Fwall_cfg.yaml") as f6:             # команды настройки firewall wan2(как замена порта)
                self.commands_Fwall_cfg = yaml.safe_load(f6)
            with open("commands_dmz_cfg.yaml") as f7:               # команды настройки DMZ доделать правило трафика!!!
                self.commands_dmz_cfg = yaml.safe_load(f7)
            with open("commands_reset_cfg.yaml") as f8:             # команды настройки reset
                self.commands_reset_cfg = yaml.safe_load(f8)
            with open("commands_sh_base.yaml") as f9:               # команды настройки base_cfg
                self.commands_sh_base = yaml.safe_load(f9)
            with open("commands_vlan_cfg.yaml") as f10:              # команды настройки vlan_cfg
                self.commands_vlan_cfg = yaml.safe_load(f10)
            with open("commands_cfg_WiFi_AP.yaml") as f11:            #  команды настройки wifi_ap
                self.commands_cfg_WiFi_AP = yaml.safe_load(f11)
            with open("commands_cfg_WiFi_AP_KingKong.yaml") as f12:    # команды настройки wifi_ap2
                self.commands_cfg_WiFi_AP_KingKong = yaml.safe_load(f12)
            with open("commands_pppoe_client_cfg.yaml") as f13:        # команды настройки РРРРоЕ-клиент
                self.commands_pppoe_client_cfg = yaml.safe_load(f13)
            with open("commands_pppoe_server_cfg.yaml") as f14:         # команды настройки РРРРоЕ-server
                self.commands_pppoe_server_cfg = yaml.safe_load(f14)
            with open("commands_cfg_ripv2.yaml") as f15:                # команды настройки Ripv2
                self.commands_cfg_ripv2 = yaml.safe_load(f15)
            with open("commands_cfg_ripng.yaml") as f16:                # команды настройки Ripng
                self.commands_cfg_ripng = yaml.safe_load(f16)
            with open("commands_cfg_ospfv2.yaml") as f17:
                self.commands_cfg_ospfv2 = yaml.safe_load(f17)
        except(NetmikoAuthenticationException,NetmikoTimeoutException) as error:
            print("*" * 5, "Error connection to:", device['host'], "*" * 5)


    def send_sh_command(self, device, command):

        """ФУНКЦИЯ отправки простой команды в уст-во по ssh, без импорта"""

        self.check_connection(device)         # вызов функции проверки соединения с роутером
        temp = self.ssh.send_command(command)
        result = temp
        return result


    def cfg_pass (self,device, commands, log=True):

        """ ФУНКЦИЯ изменения пароля, надо поменять так,
         чтоб можно было вводить короткий пароль без сбоя и тащить пароль со стороны, а не из кода.
         без импорта"""
        
        if log:
            console.print(f"Connect to {device['host']}...",style="success") # style переменная rich, назначает цвет выводу
        result = ''
        try:
            with ConnectHandler(**device) as ssh:
                new_pass = input("Input new pass: ")
                prompt = ssh.find_prompt()
                output = ssh.send_command(commands, expect_string="New password:", read_timeout=1)
                print(output, "****")
                if "New" in output:
                    output = ssh.send_command_timing(new_pass, read_timeout=1)
                    print(output, "****")
                    if "Bad password" not in output:
                        pass
                    else:
                        output = ssh.send_command_timing(new_pass, read_timeout=1)
                        console.print(output,style="success")
                    if "Re-enter new password:" in output:
                        output = ssh.send_command_timing(new_pass, read_timeout=1)
                        console.print(output,style="warning")
                        while True:
                            if "root@" not in output:
                                output = ssh.read_until_pattern(f'{prompt}', read_timeout=0)
                                print("Wait, the password will change now")
                                ssh.write_channel(" ")
                            elif "root@" in output:
                                console.print("New pass OK",style="success")
                                break
            return output
        except (NetmikoAuthenticationException, NetmikoTimeoutException) as error:
            print("*" * 5, "Error connection to:", device['host'], "*" * 5)


    def ping_inet(self, device):

        """ФУНКЦИЯ для простого пинга,  запросит адрес назначения, формат команды прописан в инит.
        без импорта."""

        ip_for_ping = "8.8.8.8"
        command_ping = (self.word_ping + ip_for_ping + self.promo)
        print(command_ping)
        output = self.ssh.send_command(command_ping)
        if "round-trip min/avg/max" in output:
            output = re.search(r'round-trip min/avg/max = (\S+ ..)', output).group()
            result = ["IP", ip_for_ping, "destination available :", output]
            result = ' '.join(result)
        else:
            result = ["Ip", ip_for_ping, "out of destination"]
            result = ' '.join(result)
        return result
        print(output)


    def ping_ip(self, device,ip_for_ping):
        command_ping = (self.word_ping + ip_for_ping + self.promo)
        print(command_ping)
        output = self.ssh.send_command(command_ping)
        if "round-trip min/avg/max" in output:
            output = re.search(r'round-trip min/avg/max = (\S+ ..)', output).group()
            result = ["IP", ip_for_ping, "destination available :", output]
            result = ' '.join(result)
        else:
            result = ["Ip", ip_for_ping, "out of destination"]
            result = ' '.join(result)
        return result
        print(output)

        """ФУНКЦИЯ для простого пинга,  запросит адрес назначения, формат команды прописан в инит.
        без импорта."""


    def tracert_ip(self,device):

        """ФУНКЦИЯ для простого tracert"""

        ip_tracert = '8.8.8.8'
        promt_tracert = '-m 3'
        comand_tracert = f'traceroute {ip_tracert} {promt_tracert}'
        output_tracert = self.ssh.send_command(comand_tracert)
        if "ms" in output_tracert:
            temp = self.send_sh_command(device,'ip a')
            output1 = re.search(r'\s+inet (?P<ip_int>\d+.\d+.\d+.\d+) peer (?P<ip_peer>\d+.\d+.\d+.\d+).{0,}pppoe-wan',
                               temp)
            ip_peer = output1.group('ip_peer')
            result = f'### Tracert passes through server-peer, {ip_peer}! ###\n {output_tracert}'

        else:
            result = f'Tracert does not pass through {output_tracert}'

        return result
        print(output)


    def reset_conf(self,device, comm_reset_conf):
        
        """ ФУНКЦИЯ сброса конфига на заводской, с ребутом устр-ва.
        без импорта
        """

        output = self.ssh.send_command("uci show system.@system[0].hostname")
        print(output)
        if "DUT" in output:
            result_reset=self.ssh.send_config_set(self.commands_to_reset_conf)
            return result_reset


    def cfg_LTE(self, device, command_cfg_3G):
        
        """ФУНКЦИЯ настройки 3G, с ребутом уср-ва.
        без импорта"""
        
        for comm in self.commands_cfg_3G:
            output = self.ssh.send_config_set(comm)
            print (output)


    def sh_base_cfg_BM10(self, device, commands_sh_base, log=True):

        """
        ФУНКЦИЯ просмотра базового конфига,вывод в виде таблицы
        """

        if log:
            console.print(f"Connect to {device['host']}...", style="warning")
        try:
            with ConnectHandler(**device) as ssh:
                console.print(device['host'], "connected!", style='success')
                for command in self.commands_sh_base:
                    if command == "route":
                        output = self.ssh.send_command(command)
                        console.print(output, style='success')
                    else:
                        sp_dev = []
                        sp_lan = []
                        sp_wan = []
                        sp_lte = []
                        sp_dev_v = []
                        sp_dev_v1 = []
                        sp_wire = []
                        sp_hn = []
                        result = {}
                        output = self.ssh.send_command(command).split('\n')
                        # output = output.replace('=', '":"')
                        # output = output.replace('\n', '","')
                        # output = ('{"' + output + '"}')         # доводим внешний вид до словаря
                        # result = json.loads(output)         # переделываем строку в словарь
                        for line in output:
                            # 1.Hostname
                            if '.hostname' in line:
                                interf = 'Host \nname'
                                data_interf = (line.split('=')[1])  # сплитуем значение после знака равно
                                sp_hn.append(data_interf)  # добавляем полученное значение в список
                                str_hn = " ".join(map(str, sp_hn))  # объединяем список строк в строку
                                result[interf] = str_hn + "\n"  # делаем словарь из ключа и значения в строке
                                if 'BWOS' in data_interf:
                                    console.print("No base cfg!", style='fail')
                            # 2.LTE status
                            if 'network.LTE.' in line:
                                interf = 'LTE'
                                data_interf = (line.split('=')[1])  # сплитуем значение после знака равно
                                sp_lte.append(data_interf)  # добавляем полученное значение в список
                                str_lte = " ".join(map(str, sp_lte))  # объединяем список строк в строку
                                result[interf] = str_lte + "\n"  # делаем словарь из ключа и значения в строке
                            # 3.WAN
                            if 'network.wan.' in line:
                                interf = 'WAN'
                                data_interf = (line.split('=')[1])  # сплитуем значение после знака равно
                                sp_wan.append(data_interf)  # добавляем полученное значение в список
                                str_wan = " ".join(map(str, sp_wan))  # объединяем список строк в строку
                                result[interf] = str_wan + "\n"  # делаем словарь из ключа и значения в строке
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
                                        data_interf = (line.split('=')[1])  # сплитуем значение после знака равно
                                        sp_fw.append(data_interf)  # добавляем полученное значение в список
                                        str_fw = " ".join(map(str, sp_fw))  # объединяем список строк в строку
                                        result[
                                            interf] = "LAN input" + str_fw + "\n"  # делаем словарь из ключа и значения в строке
                                    if "output" in line:
                                        str_fw = []
                                        sp_fw = []
                                        data_interf = (line.split('=')[1])  # сплитуем значение после знака равно
                                        sp_fw.append(data_interf)  # добавляем полученное значение в список
                                        str_fw = " ".join(map(str, sp_fw))  # объединяем список строк в строку
                                        result[
                                            interf] = "LAN output" + str_fw + "\n"  # делаем словарь из ключа и значения в строке
                                    if "forward" in line:
                                        data_interf = (line.split('=')[1])  # сплитуем значение после знака равно
                                        str_fw = []
                                        sp_fw = []
                                        sp_fw.append(data_interf)  # добавляем полученное значение в список
                                        str_fw = " ".join(map(str, sp_fw))  # объединяем список строк в строку
                                        result[
                                            interf] += "LAN forward" + str_fw + "\n"  # делаем словарь из ключа и значения в строке
                            if 'firewall.@zone' in line:
                                if "[1]" in line:
                                    interf = 'Firewall_zone_WAN'
                                    if "input" in line:
                                        data_interf = (line.split('=')[1])  # сплитуем значение после знака равно
                                        str_fw = []
                                        sp_fw = []
                                        sp_fw.append(data_interf)  # добавляем полученное значение в список
                                        str_fw = " ".join(map(str, sp_fw))  # объединяем список строк в строку
                                        result[
                                            interf] = "WAN input" + str_fw + "\n"  # делаем словарь из ключа и значения в строке
                                    if "output" in line:
                                        data_interf = (line.split('=')[1])  # сплитуем значение после знака равно
                                        str_fw = []
                                        sp_fw = []
                                        sp_fw.append(data_interf)  # добавляем полученное значение в список
                                        str_fw = " ".join(map(str, sp_fw))  # объединяем список строк в строку
                                        result[
                                            interf] = "WAN output" + str_fw + "\n"  # делаем словарь из ключа и значения в строке
                                    if "forward" in line:
                                        data_interf = (line.split('=')[1])  # сплитуем значение после знака равно
                                        str_fw = []
                                        sp_fw = []
                                        sp_fw.append(data_interf)  # добавляем полученное значение в список
                                        str_fw = " ".join(map(str, sp_fw))  # объединяем список строк в строку
                                        result[
                                            interf] += "WAN forward" + str_fw + "\n"  # делаем словарь из ключа и значения в строке
                            # 7.LAN
                            if 'network.lan.' in line:
                                interf = 'LAN'
                                data_interf = (line.split('=')[1])  # сплитуем значение после знака равно
                                sp_lan.append(data_interf)  # добавляем полученное значение в список
                                str_lan = " ".join(map(str, sp_lan))  # объединяем список строк в строку
                                result[interf] = str_lan + "\n"  # делаем словарь из ключа и значения в строке
                            # 8. Device
                            if 'network.@device[0].' in line:
                                interf = 'device'
                                data_interf = (line.split('=')[1])  # сплитуем значение после знака равно
                                sp_dev.append(data_interf)  # добавляем полученное значение в список
                                str_dev = " ".join(map(str, sp_dev))  # объединяем список строк в строку
                                result[interf] = str_dev + "\n"  # делаем словарь из ключа и значения в строке
                            # 9. Bridge-vlan
                            if 'network.@bridge-vlan[0]' in line:
                                if 'network.@bridge-vlan[0].vlan' in line:
                                    vlan_name = (line.split('=')[1])
                                    interf = format(f"bridge_Vlan{vlan_name}")
                                data_interf = (line.split('=')[1])  # сплитуем значение после знака равно
                                sp_dev_v.append(data_interf)  # добавляем полученное значение в список
                                str_dev_v = " ".join(map(str, sp_dev_v))  # объединяем список строк в строку
                                result[interf] = str_dev_v + "\n"  # делаем словарь из ключа и значения в строке
                            # 10. Bridge 2
                            if 'network.@bridge-vlan[1]' in line:
                                if 'network.@bridge-vlan[1].vlan' in line:
                                    vlan_name = (line.split('=')[1])
                                    interf = format(f"bridge_Vlan{vlan_name}")
                                data_interf = (line.split('=')[1])  # сплитуем значение после знака равно
                                sp_dev_v1.append(data_interf)  # добавляем полученное значение в список
                                str_dev_v1 = " ".join(map(str, sp_dev_v1))  # объединяем список строк в строку
                                result[interf] = str_dev_v1 + "\n"  # делаем словарь из ключа и значения в строке
                if command == "route":
                    output = self.ssh.send_command(command)
                    # console.print(output, style='success')
            list_value = list(result.values())
            str_value = ', '.join(list_value)

            c = Console()
            table = Table()
            for name, date in result.items():
                table.add_column(name)
            col_val = len(list_value)
            table.add_row(
                list_value[0], list_value[1], list_value[2],
                list_value[3], list_value[4], list_value[5],
                list_value[6]
            )
            c.print(table)
        except (NetmikoAuthenticationException, NetmikoTimeoutException) as error:
            console.print("*" * 5, "Error connection to:", device['host'], "*" * 5, style='fail')


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

    def show_int3G(self,device, command_sh_net):

        """
        ФУНКЦИЯ просмотра интерфейса 3G, с проверкой выдачи адреса
        """

        self.check_connection(device)         # вызов функции проверки соединения с роутером
        temp = self.ssh.send_config_set(command_sh_net)
        result = ""
        for line in temp:
            if "LTE.device" in temp:
                name_intf = re.search(r'network.(\S+).device', temp).group()
                result += name_intf
                temp = self.ssh.send_command("ifconfig |grep -A 1 eth1")

                if "addr:" in temp:
                    ip_int = re.search(r'inet addr:(\S+)', temp).group()
                    result +=  ip_int

                else:
                    result = name_intf
                    print("*" * 30)
                    print(name_intf, "exist, but d'nt have ip addr")
                break
            else:
                type(temp) == 'None'
                result = "No interface on router"
        return result


    def base_cfg(self, device, commands_base_cfg,log=True):
        
        """
        ФУНКЦИЯ настройки базового конфига
        """

        if log:
            console.print(f"Connect to {device['host']}...", style="warning")
        try:
            with ConnectHandler(**device) as ssh:
                console.print(device['host'], "connected!", style='success')
                result = {}
                for command in self.commands_base_cfg:
                    output = self.ssh.send_command(command, expect_string="", read_timeout=1)
                    if "mwan3" in command:
                        result_command = "wait, please"
                        print(command, result_command)
                        time.sleep(3)
                    if "commit" in command:
                        result_command = "wait, please"
                        print(command, result_command)
                        time.sleep(3)
                    if "" in output:
                        output = "command passed"
                        result[command] = output
                    elif "Usage: uci [<options>] <command> [<arguments>]" in output:
                        output = "bad command"
                        result[command] = output
                return result
        except (NetmikoAuthenticationException, NetmikoTimeoutException) as error:
            console.print("*" * 5, "Error connection to:", device['host'], "*" * 5, style='fail')


    def base_802_cfg(self, device, commands_802_1d_cfg):

        """ФУНКЦИЯ настройки stp- конфига"""

        result = {}
        for command in self.commands_802_1d_cfg:
            output = self.ssh.send_command(command, expect_string="", read_timeout=1)
            time.sleep(3) # только для 802
            if "" in output:
                output = "command passed"
                result[command] = output
            elif "Usage: uci [<options>] <command> [<arguments>]" in output:
                output = "bad command"
                result[command] = output
        return result


    def vlan_cfg(self, device, commands_vlan_cfg):

        """ФУНКЦИЯ настройки vlan- конфига (vlan-сабинтерфейc)"""

        result = {}
        for command in self.commands_vlan_cfg:
            output = self.ssh.send_command(command, expect_string="", read_timeout=2)
            if "tracking is active" in output:
                print(output)
                # output = self.ssh.send_command(command="mwan3 stop")
                console.print("mwan active!",style="fail")
                output = self.ssh.send_command(command_string="mwan3 stop", read_timeout=10)
                output = self.ssh.send_command(command_string="uci commit", read_timeout=10)
                result["mwan stop"] = output
            if "" in output:
                output = "command passed"
                result[command] = output
            elif "Usage: uci [<options>] <command> [<arguments>]" in output:
                output = "bad command"
                result[command] = output
        return result


    def utilCPU(self, device):
        result = {}
        for command in self.commands_utilCPU_cfg:
            output = self.ssh.send_command(command, expect_string="", read_timeout=1)
            time.sleep(3)  # только для 802
            if "" in output:
                output = "command passed"
                result[command] = output
            elif "Usage: uci [<options>] <command> [<arguments>]" in output:
                output = "bad command"
                result[command] = output
        return result


    def cfg_WiFi_AP(self, device, commands_cfg_WiFi_AP):

        """ФУНКЦИЯ настройки Wifi_AP"""

        result = {}
        for command in self.commands_cfg_WiFi_AP:
            output = self.ssh.send_command(command, expect_string="", read_timeout=1)
            if "" in output:
                output = "command passed"
                result[command] = output
            elif "Usage: uci [<options>] <command> [<arguments>]" in output:
                output = "bad command"
                result[command] = output
        return result
        
    def cfg_WiFi_AP_KingKong(self, device, commands_cfg_WiFi_AP_KingKong):

        """ФУНКЦИЯ настройки Wifi_AP 2 - настраиваем мост с Bulat-Free"""

        result = {}
        for command in self.commands_cfg_WiFi_AP_KingKong:
            output = self.ssh.send_command(command, expect_string="", read_timeout=1)
            if "" in output:
                output = "command passed"
                result[command] = output
            elif "Usage: uci [<options>] <command> [<arguments>]" in output:
                output = "bad command"
                result[command] = output
        temp_reboot = self.ssh.send_command("reboot", expect_string="", read_timeout=1)
        print(temp_reboot, "i am in reboot..")
        return result


    def pppoe_client_cfg(self,  device, commands_pppoe_client_cfg):
        
        """ФУНКЦИЯ настройки роутера как РРРоЕ-клиент на wan порту
        Сначала залить сервер, потом - клиент"""
        
        result = {}
        for command in self.commands_pppoe_client_cfg:
            output = self.ssh.send_command(command, expect_string="", read_timeout=1)
            if "mwan3" or "uci commit" or"reboot" in command:
                time.sleep(3)
            if "" in output:
                output = "command passed"
                result[command] = output
            elif "Usage: uci [<options>] <command> [<arguments>]" in output:
                output = "bad command"
                result[command] = output
        return result


    def pppoe(self):

        """1-ФУНКЦИЯ настройки роутера как РРРоЕ-server на wan порту
        Сервр льем первым!
        эта ф-я передает файл pppoe в DUT, в файле лежат настройки сервера ррре"""

        host = '192.168.1.1'
        user = 'root'
        secret = 'root'
        port = 22
        ssh = SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) # ключ добавится автоматом, без этого не соединится по ссх
        #ssh.load_system_host_keys()
        ssh.connect(hostname=host, username=user, password=secret, port=port)
        # SCPCLient takes a paramiko transport as an argument
        scp = SCPClient(ssh.get_transport())
        scp.put('/home/ssw/new/New_Rep/Avtomat/BM10/pppoe_cfg_file/pppoe', '/etc/config/')
        scp.close()
        ssh.close()


    def pppoe_serv_opt(self):
        
        """2-ФУНКЦИЯ настройки роутера как РРРоЕ-server на wan порту
        Сервр льем первым!
        эта ф-я передает файл pppoe-server-options в DUT, в файле лежит require-chaр,echo-interval"""
        
        host = '192.168.1.1'
        user = 'root'
        secret = 'root'
        port = 22
        ssh = SSHClient()
        ssh.set_missing_host_key_policy(
            paramiko.AutoAddPolicy())  # ключ добавится автоматом, без этого не соединится по ссх
        # ssh.load_system_host_keys()
        ssh.connect(hostname=host, username=user, password=secret, port=port)
        # SCPCLient takes a paramiko transport as an argument
        scp = SCPClient(ssh.get_transport())
        scp.put('/home/ssw/new/New_Rep/Avtomat/BM10/pppoe_cfg_file/pppoe-server-options', '/etc/ppp/')
        scp.close()
        ssh.close()


    def pppoe_chap(self,  device, commands_pppoe_server_cfg):
        
        """2-ФУНКЦИЯ настройки роутера как РРРоЕ-server на wan порту
        Сервр льем первым!
        эта ф-я передает файл chap-secrets в DUT, в файле лежит login-pass"""
        
        host = '192.168.1.1'
        user = 'root'
        secret = 'root'
        port = 22
        ssh = SSHClient()
        ssh.set_missing_host_key_policy(
            paramiko.AutoAddPolicy())  # ключ добавится автоматом, без этого не соединится по ссх
        # ssh.load_system_host_keys()
        ssh.connect(hostname=host, username=user, password=secret, port=port)
        # SCPCLient takes a paramiko transport as an argument
        scp = SCPClient(ssh.get_transport())
        scp.put('/home/ssw/new/New_Rep/Avtomat/BM10/pppoe_cfg_file/chap-secrets', '/etc/ppp/')
        scp.close()
        ssh.close()
        result = {}
        for command in self.commands_pppoe_server_cfg:
            output = self.ssh.send_command(command, expect_string="", read_timeout=1)
            if "mwan3" or "uci commit" or "reboot" in command:
                time.sleep(3)
            if "" in output:
                output = "command passed"
                result[command] = output
            elif "Usage: uci [<options>] <command> [<arguments>]" in output:
                output = "bad command"
                result[command] = output
        return result


    def cfg_ripv2(self, device, commands_ripv2_cfg):
        
        """
        ФУНКЦИЯ настройки RIPv2
        """
        
        result = {}
        for command in self.commands_cfg_ripv2:
            output = self.ssh.send_command(command, expect_string="", read_timeout=1)
            if "mwan3" in command:
                result_command = "wait, please"
                print(command, result_command)
                time.sleep(3)
            if "commit" in command:
                result_command = "wait, please"
                print(command, result_command)
                time.sleep(3)
            if "" in output:
                result_command = "command passed"
                result[command]=output
                print(command,result_command)
            elif "Usage: uci [<options>] <command> [<arguments>]" in output:
                result_command = "bad command"
                print(command, result_command)
                result[command] = result_command
        #return result


    def cfg_ripvng(self, device, commands_cfg_ripng):
        
        """
        ФУНКЦИЯ настройки RIPng
        """
        
        result = {}
        self.check_connection(device)        # вызов функции проверки соединения с роутером
        for command in self.commands_cfg_ripng:
            output = self.ssh.send_command(command, expect_string="", read_timeout=1)
            if "mwan3" in command:
                result_command = "wait, please"
                print(command, result_command)
                time.sleep(3)
            if "commit" in command:
                result_command = "wait, please"
                print(command, result_command)
                time.sleep(3)
            if "" in output:
                result_command = "command passed"
                result[command]=output
                print(command,result_command)
            elif "Usage: uci [<options>] <command> [<arguments>]" in output:
                result_command = "bad command"
                print(command, result_command)
                result[command] = result_command
        #return result


    def cfg_ospfv2(self, device, commands_cfg_ripng):
            
            """
            ФУНКЦИЯ настройки OSPFv2
            """
            
            result = {}
            self.check_connection(device)        # вызов функции проверки соединения с роутером
            for command in self.commands_cfg_ospfv2:
                output = self.ssh.send_command(command, expect_string="", read_timeout=1)
                if "mwan3" in command:
                    result_command = "wait, please"
                    print(command, result_command)
                    time.sleep(3)
                if "commit" in command:
                    result_command = "wait, please"
                    print(command, result_command)
                    time.sleep(3)
                if "" in output:
                    result_command = "command passed"
                    result[command]=output
                    print(command,result_command)
                elif "Usage: uci [<options>] <command> [<arguments>]" in output:
                    result_command = "bad command"
                    print(command, result_command)
                    result[command] = result_command
            #return result


    '''
    ПОСЛЕ этого класса не писать ф-ии для Роутер1 - object has no attribute!!!!!!
    Класс и функция проверки ошибок - дописать 
    '''
    
class ErrorInCommand(Exception):
    """
    Исключение генерируется, если при выполнении команды на оборудовании,
    возникла ошибка.
    """
    def _check_error_in_command(self, command, result):
        regex = "Usage (?P<err>.+)"
        message = (
            'При выполнении команды "{cmd}" на устройстве {device} возникла ошибка "{error}"'
        )
        error_in_cmd = re.search(regex, result)
        if error_in_cmd:
            raise ErrorInCommand(message.format(cmd=command, device=self.host, error=error_in_cmd.group('err')))
        print ()

if __name__ == "__main__":
    with open("BM10_LTE.yaml")as f:
         temp = yaml.safe_load(f)
         for t in temp:
            device = dict(t)
            r1 = Router(**device)
            # host = '192.168.1.1'
            # user = 'root'
            # password = 'root'
            # port = 22
            print(r1.ping_ip(device,ip_for_ping='2.2.2.2'))                  # Ping ip
            #print(r1.ping_inet(device))                                      # Ping inet (8.8.8.8)
            #print(r1.reset_conf(device,r1.commands_to_reset_conf))         # Reset conf
            #print(r1.sh_base_cfg_BM10(device, r1.commands_sh_base))        # Show base_cfg TABLE!
            #print(r1.show_int3G(device,"uci show network | grep LTE"))     # Show LTE
            #print(r1.check_connection(device))
            #print(r1.cfg_LTE(device,r1.commands_cfg_3G))                   # Cfg LTE
            #print(r1.cfg_pass(device,commands="passwd"))                   # Cfg pass
            #print(r1.vlan_cfg(device,r1.commands_vlan_cfg))                # Cfg vlan
            #print(r1.base_cfg(device, r1.commands_base_cfg))               # Cfg base_cfg (wan-st_ip, fire,name)
            #print (r1.base_802_cfg(device, r1.commands_802_1d_cfg))        # Cfg for 802d (STP)
            #print (r1.base_cfg(device, r1.commands_dmz_cfg))               # Cfg for DMZ
            #print (r1.base_cfg(device, r1.commands_gre_config))            # Cfg for test GRE
            #print (r1.base_cfg(device, r1.commands_Fwall_cfg))             # Cfg for test firewall
            #print(r1.send_sh_command(device,"uci show"))                   # send comm uci show"
            #print(r1.send_sh_command("brctl stp br-lan yes"))              # send comm "brctl stp br-lan yes" ST
            #print(r1.cfg_WiFi_AP(device,r1.commands_cfg_WiFi_AP))           # Cfg wifi_ap (1-й порт не раздает!!!)
            #print(r1.cfg_WiFi_AP_KingKong(device,r1.commands_cfg_WiFi_AP_KingKong))    # Cfg wifi_ap_KingKong
            #print(r1.pppoe_client_cfg(device, r1.commands_pppoe_client_cfg))               # Cfg pppoe-client

            # print(r1.pppoe())                                                   # Cfg pppoe-serv f1
            # print(r1.pppoe_serv_opt())                                          # Cfg pppoe-serv f2
            # print(r1.pppoe_chap(device, r1.commands_pppoe_server_cfg))          # Cfg pppoe-serv f3
            #print (r1.tracert_ip(device))
            #print(r1.cfg_ripv2(device, r1.commands_cfg_ripv2))                  # Cfg RIPv2+base_cfg
            #print(r1.cfg_ripvng(device, r1.commands_cfg_ripng))                 # Cfg RIPng+base_cfg
            #print(r1.cfg_ospfv2(device,r1.commands_cfg_ospfv2))                  # Cfg Ospfv2+base_cfg