import re
import yaml
import netmiko
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)

def send_show_command(device, command):
    result = ''
    try:
        with ConnectHandler(**device) as ssh:
            temp = ssh.send_command(command)

            for sec in temp:
                    if "34G.device" in temp:
                        name_intf = re.search(r'network.(\S+).device', temp).group()
                        result += name_intf

                        temp = ssh.send_command("ifconfig |grep -A 1 wwan0")

                        if "addr:" in temp:
                            ip_int = re.search(r'inet addr:(\S+)', temp).group()
                            result += ip_int
                        else:
                            result = name_intf
                            print("*"*30)
                            print(name_intf," exist, but d'nt have ip addr")
                        break
                    else:
                        result="\nNo interface on router"
                        break

        return result
    except (NetmikoAuthenticationException, NetmikoTimeoutException) as error:
        print("*"*20, ERROR, "*"*20)


if __name__ == "__main__":
    command = "uci show network | grep 34G"
    with open("BM10_LTE.yaml")as f:
        device = yaml.safe_load(f)

    for dev in device:
        print(send_show_command(dev, command))
