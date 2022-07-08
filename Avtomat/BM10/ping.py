import re
import yaml
import netmiko
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)

def ping_ip_3G (device,commands, ip_dest, promo,log = True):
    if log:
        print(f"Connect to {device['host']}...")

    try:
        with ConnectHandler(**device) as ssh:
            print(device['host'], "connected")
            for command in commands:
                result=""
                output = ssh.send_command(temp)
                if "round-trip min/avg/max" in output:
                    output = re.search(r'round-trip min/avg/max = (\S+ ..)', output).group()
                    result += output
                    print("*"*30)
                    print("IP ",ip_dest, "destination  available from 3G: ",result)
                else:
                    print("*"*30)
                    print("Ip ",ip_dest, "out of destination")
        return result
    except (NetmikoAuthenticationException, NetmikoTimeoutException) as error:
        print("*"*5, "Error connection to:", device['host'], "*"*5)
if __name__ == "__main__":
    ip_dest = "8.8.8.8"
    promo= " -w 4"
    commands ="ping "
    temp = (commands+ip_dest+promo)
    print(temp)
    with open("BM10_LTE.yaml")as f:
        device = yaml.safe_load(f)
        for dev in device:
            print(ping_ip_3G(dev, commands, ip_dest, promo))




