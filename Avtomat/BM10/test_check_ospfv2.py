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
from check_ospfv2 import (check_enable_ospfv2
                         )

def test_check_enable_ospfv2():
    assert check_enable_ospfv2()==True, "OSPFv2 disable!"