import re
import yaml
import netmiko
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)
from clss_Router import Router

def check_base_cfg():
    with open("BM10_LTE.yaml")as f:
        temp = yaml.safe_load(f)
        for t in temp:
            device = dict(t)
            r1 = Router(**device)
    try:
        r1.send_sh_command(command="uci show firewall.@defaults[0].flow_offloading_hw")
        return True
    except ValueError as err:
        return False

def test_cfg_pass():
    assert check_base_cfg()==True, "OK"
    assert check_base_cfg()==False, "FAIL"


