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
from check_ripng import (check_enable_ripng,                 
                         check_route_ripng_net,
                         check_ping_interf,
                         )


def test_check_enable_ripng():
    assert check_enable_ripng()==True, "RIPng disable!"


def test_check_route_ripng(): 
    # ф-я check_route_ripng_net() в цикле переберет список маршрутов, если нужного нет-вернет false
    assert check_route_ripng_net()==True, "*** Some route to the network 2001::/64 is not available! ***"


"""
В блоке ниже используется параметризация mark.parametrize
"""
ip_for_check = (
    ('2001:10::1'),
    ('2001:10::2'),
    ('2001:20::2'),
    ('2001:30::2'),
    ('2002:10::4'),
    ('2002:20::4'),
    
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
    assert check_ping_interf(ip_for_ping=f"{ip_test}")==True, f"*** IP {ip_test} unavaileble now***"
    