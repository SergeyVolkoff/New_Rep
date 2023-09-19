import re
import yaml
import time
import netmiko
import pytest
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)
from clss_Router import Router
from check_Fwall import  check_Fwall


def test_check_Fwall():

    assert check_Fwall()==True, "Firewall zone bad config"

    #assert check_rootSTP("uci show firewall.@zone[1].forward")==True, "Firewall.@zone[1].forward disable"


