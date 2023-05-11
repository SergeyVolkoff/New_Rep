import re
import yaml
import netmiko
import pytest
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)
from clss_Router import Router
from check_base_cfg import check_sup_ASIC, check_firewall,check_name_dev

def test_enable_support_ASIC():
    assert check_sup_ASIC("uci show firewall.@defaults[0].flow_offloading_hw")==True, "Firewall offloading_hw  disable"
def test_enable_firewall_zone_wan():
    assert check_firewall("uci show firewall.@zone[1].forward")==True, "Firewall.@zone[1].forward disable"
def test_enable_name_device():
    assert check_name_dev("uci show system.@system[0].hostname")==True, "Name device is wrong"
    # assert check_base_cfg("uci show system.@system[0].hostname") ==True, "Name device is wrong"
# def test_name_device():
#     assert check_name_device("uci show system.@system[0].hostname")=True, "sdf"