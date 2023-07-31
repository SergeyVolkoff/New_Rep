import re
import yaml
import netmiko
import pytest
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)
from clss_Router import Router
from check_rootSTP import  check_rootSTP

def test_base_cfg():
    assert check_rootSTP("brctl showstp br-lan")==True, "Router is not root in STP"
    #assert check_rootSTP("uci show firewall.@zone[1].forward")==True, "Firewall.@zone[1].forward disable"

