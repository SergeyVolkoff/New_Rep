import yaml
import textfsm
from sh_base_cfg_BM10 import sh_base_cfg_BM10
from textfsm import clitable

def parse_command_dynamic(command_output, atributes_dict, index_file = "index", templ_path = "templates"):
    clitable1 = clitable.CliTable(index_file, templ_path)
    clitable1.ParseCmd(command_output, atributes_dict)
    return [ dict(zip(clitable1.header,item)) for item in clitable1]
if __name__ == "__main__":
    command = ["arp -a"]
    atributes = {"Command":"arp -a", "Vendor":"linux_os"}
    with open("BM10_LTE.yaml") as f:
        device = yaml.safe_load(f)
        for dev in device:
            output = sh_base_cfg_BM10(dev, command)

            result_clitable = parse_command_dynamic(output, atributes)
    print (result_clitable)
