import re
import yaml
import netmiko
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)
from clss_Router import Router
from check_WiFi_AP import check_WiFi_AP

def test_Wifi_AP():
    assert check_WiFi_AP("uci show network")==True, "FFF"
