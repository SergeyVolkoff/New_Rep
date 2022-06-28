

import pexpect
from pprint import pprint

def cfg_wwan_BM10(
    int_name,
    proto_value,
    device_value,
    apn_value,
    pdp_type
):
    output_show_ifcfg = send_show_ifcof("192.168.1.1", "root", "root", ["ifconfig | grep -A 1  wwan0"])
    if "ip" in output_show_ifcfg:

        pprint({int_name}"already exists")

