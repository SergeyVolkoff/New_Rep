import re
import yaml
import netmiko
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)
from clss_Router import Router
from check_int3G import check_int3G
def test_int3G():
    assert check_int3G("uci show network | grep LTE")==True, "Addr interface LTE or interface not exist"
    #assert check_int3G("uci show network | grep 34G")==False, "### test FAIL ###, int exist, but d'nt have ip addr "

