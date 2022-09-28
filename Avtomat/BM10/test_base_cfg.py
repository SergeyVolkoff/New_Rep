import re
import yaml
import netmiko
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)
from clss_Router import Router
from check_base_cfg import  check_base_cfg

def test_base_cfg():
    assert check_base_cfg("uci show firewall.@defaults[0].flow_offloading_hw")==True, "Firewall offloading_hw  disable"
    assert check_base_cfg("uci show firewall.@zone[1].forward")==True, "Firewall.@zone[1].forward disable"

