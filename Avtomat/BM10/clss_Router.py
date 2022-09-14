# -*- coding: utf-8 -*-
import re
import yaml
import netmiko
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)

class Router:
    def __init__(self, device_type, host, username, password, timeout):
        try:
            self.ssh = ConnectHandler(**device)
            self.ip = host
            self.name = username
            self.passwd = password
            self.promo = " -w 4"
            self.word_ping = "ping "
            self.command_ping = self.word_ping+self.promo
            with open ("BM10_LTE.yaml") as f2:
                self.device = yaml.safe_load(f2)
            with open ("commands_reset_cfg.yaml") as f1:
                self.commands_to_reset_conf = yaml.safe_load(f1)
            with open("commands_cfg_3G.yaml") as f:
                self.commands_cfg_3G = yaml.safe_load(f)


        except(NetmikoAuthenticationException,NetmikoTimeoutException) as error:
            print("*" * 5, "Error connection to:", device['host'], "*" * 5)
    """
    ФУНКЦИЯ отправки простой команды в уст-во по ssh, без импорта
    """
    def send_sh_command(self, command):
        temp = self.ssh.send_command(command)
        result = temp
        return result
    """
     ФУНКЦИЯ изменения пароля, надо поменять так, 
     чтоб можно было вводить короткий пароль без сбоя и тащить пароль со стороны, а не из кода.
     без импорта
    """
    def cfg_pass (sel,device, commands, log=True):
        if log:
            print(f"Connect to {device['host']}...")
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
                        print(output)
                    if "Re-enter new password:" in output:
                        output = ssh.send_command_timing(new_pass, read_timeout=1)
                        print(output)
                        while True:
                            if "root@" not in output:
                                output = ssh.read_until_pattern(f'{prompt}', read_timeout=0)
                                print("Wait, the password will change now")
                                ssh.write_channel(" ")
                            elif "root@" in output:
                                print("New pass OK")
                                break

            return output
        except (NetmikoAuthenticationException, NetmikoTimeoutException) as error:
            print("*" * 5, "Error connection to:", device['host'], "*" * 5)
    """
    ФУНКЦИЯ для простого пинга,  запросит адрес назначения, формат команды прописан в инит.
    без импорта.
    """
    def ping_ip(self, device, command_ping):
        ip_dest = input("Input ip destination: ")
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
    """
    ФУНКЦИЯ сброса конфига на заводской, с ребутом устр-ва. 
    без импорта
    """
    def reset_conf(self,device, comm_reset_conf):
        result_reset=self.ssh.send_config_set(self.commands_to_reset_conf)
        return result_reset
    """
    ФУНКЦИЯ настройки 3G, с ребутом уср-ва.
    без импорта
    """
    def cfg_LTE(self, device, command_cfg_3G):
        for comm in self.commands_cfg_3G:
            output = self.ssh.send_config_set(comm)
            print (output)
    """
    ФУНКЦИЯ просмотра интерфейса 3G
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

if __name__ == "__main__":
    with open("BM10_LTE.yaml")as f:
        temp = yaml.safe_load(f)
        for t in temp:
            device = dict(t)
            r1 = Router(**device)

            #print(r1.ping_ip(device,r1.command_ping ))
            #print(r1.reset_conf(device,r1.commands_to_reset_conf))
            #print(r1.cfg_LTE(device,r1.commands_cfg_3G))
            print(r1.show_int3G(device,"uci show network | grep 34G"))
            #print(r1.cfg_pass(device,commands="passwd"))
            #print(r1.cfg_LTE(device,r1.commands_cfg_3G))
