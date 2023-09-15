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
from check_ospfv2 import (check_enable_ospfv2,
                          check_route_ospfv2_net,
                         )

def test_check_enable_ospfv2():
    assert check_enable_ospfv2()==True, "OSPFv2 disable!"

def test_check_route_ospfv2_net(): 
    # ф-я check_route_ripng_net() в цикле переберет список маршрутов, если нужного нет - вернет false
    assert check_route_ospfv2_net()==True, "*** Some route to the network 192.. or 200.. is not available! ***"

