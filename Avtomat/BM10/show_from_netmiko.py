import yaml
import netmiko
from netmiko import ConnectHandler

def send_show_command(device, command):
    result = ''
    with ConnectHandler(**device) as ssh:
        result = ssh.send_command(command)
    return result



if __name__ == "__main__":
    command = "ifconfig"
    with open("BM10_LTE.yaml")as f:
        device = yaml.safe_load(f)

    for dev in device:
        print(send_show_command(dev, command))
