import re
import yaml
import netmiko
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)
from clss_Router import Router
class Tests (Router):
    def __init__(self,device_type, host, username, password, timeout):
        super().__init__(device_type,host, username, password, timeout)
    def test_check_int3G(self):
        assert Router.show_int3G()
if __name__ == "__main__":

    def check_

    device = Router.device
    r1=Roter(**device)
    print(r1.test_int3G(device))