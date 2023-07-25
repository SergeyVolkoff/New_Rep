import re

import pytest
import tasks
from tasks import Task
import yaml
import netmiko
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)
from clss_Router import Router
from check_pppoe_client import check_int_pppoe_cl, check_ping_inet,check_ip_pppoe,\
    check_ip_peer

def test_name_intPPPoE():
    assert check_int_pppoe_cl ("uci show network.wan.proto")==True, "No PPPoE on wan-interface!!!"
def test_check_ping_inet():
    assert check_ping_inet()== True, "Inet(8.8.8.8)- not available. Wan-port bad?"

def test_check_ip_pppoe():
    assert check_ip_pppoe('ip a')==True, "interface exist, but dont have ip, tunnel state DOWN"

#@pytest.mark.parametrize('task',Task('192.168.3.1'))
def test_check_ip_peer():
    task=Task(summary='192.168.3.1')
    assert equivalent (check_ip_peer("ip a"), task)

def equivalent (t1,t2):
    return (t1== t2.summary)