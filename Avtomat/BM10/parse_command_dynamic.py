import yaml
import textfsm
from pprint import pprint
from sh_base_cfg_BM10 import sh_base_cfg_BM10
from textfsm import clitable
import netmiko
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)
def parse_command_dynamic(command_output, atributes_dict, index_file = "index", templ_path = "templates"):
    clitable1 = clitable.CliTable(index_file, templ_path)
    clitable1.ParseCmd(command_output, atributes_dict)
    #header = list(clitable1.header)
    data = clitable1.FormattedTable()
    return data


if __name__ == "__main__":
    atributes = {"Command":"uci show", "Vendor":"linux_os"}
    command = ["uci show"]
    with open("BM10_LTE.yaml") as f:
        device = yaml.safe_load(f)
        for dev in device:
            output = sh_base_cfg_BM10(dev, command)
    result_clitable = parse_command_dynamic(output, atributes)
    pprint (result_clitable)
