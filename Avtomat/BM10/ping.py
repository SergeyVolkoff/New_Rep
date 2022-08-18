import re
import yaml
import netmiko
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)
ip_dest = "8.8.4.4"
promo= " -w 4"
word_ping="ping "
command_ping = (word_ping+ip_dest+promo)

def ping_ip (device,command_ping):
    try:
        with ConnectHandler(**device) as ssh:
            output = ssh.send_command(command_ping)
            if "round-trip min/avg/max" in output:
                output = re.search(r'round-trip min/avg/max = (\S+ ..)', output).group()
                result = ["IP", ip_dest, "destination  available :", output]
                result = ' '.join(result)
            else:
                result = ["Ip",ip_dest, "out of destination"]
                result = ' '.join(result)
        return result
    except (NetmikoAuthenticationException, NetmikoTimeoutException) as error:
        print("*"*5, "Error connection to:", device['host'], "*"*5)
if __name__ == "__main__":
    with open("BM10_LTE.yaml")as f:
        device = yaml.safe_load(f)
        for dev in device:
            print(ping_ip(dev, command_ping))




