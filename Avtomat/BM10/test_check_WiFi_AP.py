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
from check_WiFi_AP import check_WiFi_AP,check_pingGW

def test_Wifi_AP():
    assert check_WiFi_AP("uci show network.Br_AP")==True, "No interface needed"

def test_check_pingGW():
    assert check_pingGW()== True, "GW out"