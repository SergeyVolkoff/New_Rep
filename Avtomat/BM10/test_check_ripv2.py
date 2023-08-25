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
from check_ripv2 import (check_enable_ripv2,
                         check_ver_ripv2,
                         check_route_ripv2
                         )

def test_check_enable_ripv2():
    assert check_enable_ripv2()==True, "RIP disable!"

def test_check_version_ripv2():
    assert check_ver_ripv2()==True, "ver RIP not 2!"

def test_check_route_ripv2():
    assert check_route_ripv2()==True, "*** Route to the network 200.. is not available! ***"