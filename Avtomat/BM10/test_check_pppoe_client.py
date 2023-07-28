import re

import pytest
# import tasks
# from tasks import Task
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
"""
В блоке 28-51 используется параметризация mark.parametrize
"""
# @pytest.mark.parametrize('summary',
#                          [('192.168.4.1'),
#                          ('192.168.3.1'),
#                          ('192.168.1.1'),
#                         ('192.168.2.1')
#                                  ])
# def test_check_ip_peer(summary):
#     task=Task(summary)
#     assert equivalent (check_ip_peer("ip a"), task)== True, "Wrong ip"


tasks_to_check_ip = ( # заносим в переменную данные для проверки
    ('192.168.4.1'),
    ('192.168.2.1')
)
task_ids = ['ip_test({})'.format(t) # определям параметр ids чтобы сделать идентификаторы для понимания вывода теста
            for t in tasks_to_check_ip
            ]
@pytest.mark.parametrize("ip_test",tasks_to_check_ip,ids=task_ids)
#("task",tasks_to_check_ip, ids=task_ids)
# используем параметризацию,
# передаем в нее первый аргумент parametrize() — это строка с разделенным запятыми списком имен — "ip_test" в нашем случае,
# переменную указывающую на данные для проверки (tasks_to_check_ip) и ids
def test_check_ip_peer(ip_test):
    # функция вызывается многократно  с указанными аргументами ip_test
    assert equivalent(check_ip_peer("ip a"), ip_test) == True, "Wrong ip"
    # assert вызовет функцию equivalent которая проверит
    # равенство на соответствие, используя значение (True\Фолс), полученное из check_ip_peer,
    # а потом проверит внутри assertа на равенство с Труе и вернет результат
def equivalent (t1,t2):
    return (t1== t2)
