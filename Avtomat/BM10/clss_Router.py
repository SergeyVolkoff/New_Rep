# -*- coding: utf-8 -*-
import yaml
import netmiko
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)

class Router:
    def __init__(self, device_type, host, username, password, timeout):
        self.ssh = ConnectHandler(**device)
        self.ip = host
        self.name = username
        self.passwd = password

    def send_sh_command(self, command):
        temp = self.ssh.send_command(command)
        result = temp
        return result

    def cfg_pass (device, commands, log=True):
        if log:
            print(f"Connect to {device['host']}...")
        result = ''
        try:
            with ConnectHandler(**device) as ssh:
                for comm in commands:
                    prompt = ssh.find_prompt()
                    output = ssh.send_command(comm, expect_string="New password:", read_timeout=1)
                    print(output, "****")
                    if "New" in output:
                        output = ssh.send_command_timing("Qq123456", read_timeout=1)
                        print(output, "****")
                        if "Re-enter new password:" in output:
                            output = ssh.send_command_timing("Qq123456", read_timeout=1)
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
TODO
"""
    def ping_ip(device, command_ping):
        ip_dest = "8.8.8.8"
        promo = " -w 4"
        word_ping = "ping "
        self.command_ping = (word_ping + ip_dest + promo)
        output = self.ssh.send_command(command_ping)
        if "round-trip min/avg/max" in output:
            output = re.search(r'round-trip min/avg/max = (\S+ ..)', output).group()
            result = ["IP", ip_dest, "destination  available :", output]
            result = ' '.join(result)
        else:
            result = ["Ip", ip_dest, "out of destination"]
            result = ' '.join(result)
        return result

if __name__ == "__main__":
    with open("BM10_LTE.yaml")as f:
        device = yaml.safe_load(f)
        for dev in device:
            print(Router.ping_ip(device))
