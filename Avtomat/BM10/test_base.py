import re
import yaml
import netmiko
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)
from clss_Router import Router

def check_int3G(comm):
    with open("BM10_LTE.yaml")as f:
        temp = yaml.safe_load(f)
        for t in temp:
            device = dict(t)
            r1 = Router(**device)
    try:
        r1.show_int3G(device,comm)
        return True
    except ValueError as err:
        return False

def test_int3G():
    assert check_int3G("uci show network | grep 34G")==True, "Test OK"
    #assert check_int3G("dgx")==False, "test FAIL"

if __name__ =="__main__":

    result = check_int3G("uci show network | grep 34G")
    print (result)
