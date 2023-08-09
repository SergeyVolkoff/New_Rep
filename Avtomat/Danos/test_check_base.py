import re
import pytest
import yaml
import netmiko
from netmiko import  (
ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException
)
from cls_Danos import Danos
from check_base_cfg import check_ok_hostname


value_check_name = (
    ('set system host-name A'),
    ('set system host-name Av'),
    ('set system host-name Ave'),
    ('set system host-name Ave_'),
    ('set system host-name Ave?'),
    ('set system host-name %'),
    ('set system host-name Aggregation-switch-DUT-Aggregation-switch-DUT-Aggregation-switcH'),
    ('set system host-name Aggregation-switch-DUT-Aggregation-switch-DUT-Aggregation-switc'),
)

task_ids = [
    'ip_test({})'.format(t)
     for t in value_check_name
            ]
@pytest.mark.parametrize("ip_test", value_check_name,ids=task_ids)
def test_check_base(ip_test):
    assert (check_ok_hostname(ip_test)) == True, "Wrong name"



