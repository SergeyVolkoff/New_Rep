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
from check_workSTP import  check_workSTP
def test_base_cfg():

    assert check_workSTP("logread -l 10")==True, "STP is not work"

    #assert check_rootSTP("uci show firewall.@zone[1].forward")==True, "Firewall.@zone[1].forward disable"

