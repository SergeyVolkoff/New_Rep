import yaml
from pprint import pprint
from send_sh_comm import send_sh_comm
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)
def cfg_passwd(device, new_passwd):
    result_cfg_passwd = send_sh_comm (dev, comm_new_pass, expect_string ="password:")
    print(result_cfg_passwd)
if __name__== "__main__":
    comm_new_pass = [
        "passwd",
        "root1",
        "root1"
    ]
    with open("BM10_LTE.yaml") as f:
        device = yaml.safe_load(f)
        for dev in device:
            cfg_passwd(dev, comm_new_pass)