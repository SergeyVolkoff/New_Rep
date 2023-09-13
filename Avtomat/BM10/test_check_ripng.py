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
                         check_route_ripng_net
                         )

def test_check_enable_ripng():
    assert check_enable_ripng()==True, "RIPng disable!"


def test_check_route_ripng(): 
    # ф-я check_route_ripng_net() в цикле переберет список маршрутов, если нужного нет - вернет false
    assert check_route_ripng_net()==True, "*** Some route to the network 2001::/64 is not available! ***"

