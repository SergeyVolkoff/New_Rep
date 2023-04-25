import re
import yaml
import netmiko
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)
from clss_Router import Router
from check_802Q import check_vln_cfg
def test_802Q():
    assert check_vln_cfg("uci show network") ==True, "Interface vlan 2 or 3 not exist"
