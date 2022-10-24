# -*- coding: utf-8 -*-
import re
import yaml
import netmiko
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
from rich.console import Console
from rich.table import Table
from netmiko.linux.linux_ssh import LinuxSSH


my_colors = Theme( #добавляет цветовую градацию для rich
    {
        "success":"bold green",
        "fail":"bold red",
        "warning":"bold yellow"
    }
)
console = Console(theme=my_colors)

class Router():
    def __init__(self, device_type, host, username, password, timeout, **kwargs):
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

        except(NetmikoAuthenticationException,NetmikoTimeoutException) as error:
            print("*" * 5, "Error connection to:", device['host'], "*" * 5)
    """
    ФУНКЦИЯ отправки простой команды в уст-во по ssh, без импорта
    """
    def send_sh_command(self, device, command):
        temp = self.ssh.send_command(command)
        result = temp
        return result
    """
     ФУНКЦИЯ изменения пароля, надо поменять так, 
     чтоб можно было вводить короткий пароль без сбоя и тащить пароль со стороны, а не из кода.
     без импорта
    """
    def cfg_pass (self,device, commands, log=True):
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
    """
    ФУНКЦИЯ для простого пинга,  запросит адрес назначения, формат команды прописан в инит.
    без импорта.
    """
    def ping_ip(self, device, command_ping):
        ip_dest = '200.1.1.1'
        command_ping = (self.word_ping + ip_dest + self.promo)
        print(command_ping)
        output = self.ssh.send_command(command_ping)
        if "round-trip min/avg/max" in output:
            output = re.search(r'round-trip min/avg/max = (\S+ ..)', output).group()
            result = ["IP", ip_dest, "destination  available :", output]
            result = ' '.join(result)
        else:
            result = ["Ip", ip_dest, "out of destination"]
            result = ' '.join(result)
        return result
        print(output)

    """
    ФУНКЦИЯ сброса конфига на заводской, с ребутом устр-ва. 
    без импорта
    """
    def reset_conf(self,device, comm_reset_conf):
        result_reset=self.ssh.send_config_set(self.commands_to_reset_conf)
        return result_reset
    """
    ФУНКЦИЯ настройки 3G, с ребутом уср-ва.
    без импорта    """
    def cfg_LTE(self, device, command_cfg_3G):
        for comm in self.commands_cfg_3G:
            output = self.ssh.send_config_set(comm)
            print (output)

    """
     !!!!! ДОДЕЛАТЬ!!!!
      ФУНКЦИЯ просмотра базового конфига
    """
    def show_base_cfg(self, device, command_sh_net):
        temp = self.ssh.send_config_set(command_sh_net)
        result = {}
        for sec in temp:
            if "network.lan" in temp:
                name_intf = re.search(r'network.(\S+).device', temp).group()
                result += name_intf
                temp = self.ssh.send_command("ifconfig |grep -A 1 wwan0")

                if "addr:" in temp:
                    ip_int = re.search(r'inet addr:(\S+)', temp).group()
                    result += ip_int

                else:
                    result = name_intf
                    print("*" * 30)
                    print(name_intf, "exist, but d'nt have ip addr")
                break
            else:
                type(temp) == 'None'
                result = "No interface on router"
        table = Table()
        for n in result.split():
            table.add_column(n)
        return result

    """
    ФУНКЦИЯ просмотра интерфейса 3G, с проверкой выдачи адреса
    """
    def show_int3G(self,device, command_sh_net):
        temp = self.ssh.send_config_set(command_sh_net)
        result = ""
        for sec in temp:
            if "34G.device" in temp:
                name_intf = re.search(r'network.(\S+).device', temp).group()
                result += name_intf
                temp = self.ssh.send_command("ifconfig |grep -A 1 wwan0")

                if "addr:" in temp:
                    ip_int = re.search(r'inet addr:(\S+)', temp).group()
                    result += ip_int

                else:
                    result = name_intf
                    print("*" * 30)
                    print(name_intf, "exist, but d'nt have ip addr")
                break
            else:
                type(temp) == 'None'
                result = "No interface on router"
        return result

    """
    ФУНКЦИЯ настройки базового конфига
    """
    def base_cfg(self, device, commands_base_cfg):
        result = {}
        for command in self.commands_base_cfg:
            output = self.ssh.send_command(command, expect_string="", read_timeout=1)
            time.sleep(1)
            if "" in output:
                output = "command passed"
                result[command] = output
            elif "Usage: uci [<options>] <command> [<arguments>]" in output:
                output = "bad command"
                result[command] = output
        return result
    '''
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
            #print(r1.ping_ip(device,r1.command_ping ))
            #print(r1.reset_conf(device,r1.commands_to_reset_conf))
            #print(r1.cfg_LTE(device,r1.commands_cfg_3G))
            #print(r1.show_int3G(device,"uci show network | grep 34G"))
            #print(r1.cfg_pass(device,commands="passwd"))
            #print(r1.cfg_LTE(device,r1.commands_cfg_3G))
            print(r1.base_cfg(device, r1.commands_base_cfg))
            # print (r1.base_cfg(device, r1.commands_802_1d_cfg))
            #print (r1.base_cfg(device, r1.commands_gre_config))
            #print (r1.base_cfg(device, r1.commands_Fwall_cfg))
            #print(r1.send_sh_command(device,"uci show"))
            #print(r1.send_sh_command("brctl stp br-lan yes"))
