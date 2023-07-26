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

# @pytest.mark.parametrize('summary',
#                          [('192.168.4.1'),
#                          ('192.168.3.1'),
#                          ('192.168.1.1'),
#                         ('192.168.2.1')
#                                  ])
# def test_check_ip_peer(summary):
#     task=Task(summary)
#     assert equivalent (check_ip_peer("ip a"), task)== True, "Wrong ip"


tasks_to_check_ip = (
    Task('192.168.4.1'),
    Task('192.168.2.1')
)
task_ids = ['Task({})'.format(t.summary)
            for t in tasks_to_check_ip
            ]
@pytest.mark.parametrize("task",tasks_to_check_ip, ids=task_ids)
def test_check_ip_peer(task):
    #task = Task(task)
    assert equivalent(check_ip_peer("ip a"), task) == True, "Wrong ip"
def equivalent (t1,t2):
    return (t1== t2.summary)
