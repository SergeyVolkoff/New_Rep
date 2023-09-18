import re

import pytest
import yaml
import netmiko
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)
from clss_Router import Router
from check_ripv2 import (check_enable_ripv2,
                         check_ver_ripv2,
                         check_route_ripv2,
                         check_ping_interf,
                         )

def test_check_enable_ripv2():
    assert check_enable_ripv2()==True, "RIP disable!"

def test_check_version_ripv2():
    assert check_ver_ripv2()==True, "ver RIP not 2!"

def test_check_route_ripv2():
    assert check_route_ripv2()==True, "*** Route to the network 200.. is not available! ***"


"""
В блоке ниже используется параметризация mark.parametrize
"""
ip_for_check = (
    ('192.168.1.1'),
    ('192.168.10.1'),
    ('192.168.10.2'),
    ('192.168.20.1'),
    ('192.168.20.2'),
    ('200.1.10.2'),
    ('200.1.20.2'),
    
)
task_ids = ['ip_test({})'.format(t)
             # определям параметр ids чтобы сделать идентификаторы для понимания вывода теста
            for t in ip_for_check
            ]
@pytest.mark.parametrize("ip_test",ip_for_check,ids=task_ids)
            #("ip_test",ip_for_check,ids=task_ids)
            # используем параметризацию,
            # передаем в нее первый аргумент parametrize() — это строка с разделенным
            # запятыми списком имен — "ip_test" в нашем случае,
            # переменную указывающую на данные для проверки (ip_for_check) и ids

def test_check_ping_inter(ip_test):
    assert check_ping_interf(ip_for_ping=f"{ip_test}")==True, f"*** IP {ip_test} unavaileble now ***"
    