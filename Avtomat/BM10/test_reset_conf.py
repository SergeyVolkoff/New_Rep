import yaml
from pprint import pprint
from send_sh_comm import send_sh_comm
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)

def reset_conf(device, reset_conf):
    result_reset = send_sh_comm(dev, comm_reset_conf)
    print (result_reset)
if __name__ == "__main__":
    comm_reset_conf = [
    "rm -rf /overlay/*",
    "sync",
    "reboot"
    ]
    with open ("BM10_LTE.yaml")as  f:
        device = yaml.safe_load(f)
        for dev in device:
            reset_conf(dev,comm_reset_conf)