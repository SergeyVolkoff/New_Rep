import yaml
from pprint import pprint
from base_cfg_BM10_HP import base_cfg

if __name__ == "__main__":
    commands = [
    "uci set network.wan.proto='dhcp'",
    "uci commit",
    "ifdown wan",
    "ifup wan"
    ]
    print(commands)
    with open("BM10_LTE.yaml") as f:
        device = yaml.safe_load(f)
        for dev in device:
            pprint(base_cfg(dev, commands))