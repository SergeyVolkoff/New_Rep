import yaml
from pprint import pprint
from send_sh_comm import send_sh_comm
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)
from netmiko import *


def cfg_pass (device, commands, log = True):
    new_pass = input("Input new pass: ")
    if log:
        print(f"Connect to {device['host']}...")
    result = ''
    try:
        with ConnectHandler(**device) as ssh:
            prompt = ssh.find_prompt()
            output = ssh.send_command(commands, expect_string="New password:", read_timeout=1)
            print(output, "****")
            if "New" in output:
                output = ssh.send_command_timing(new_pass, read_timeout=1)
                print(output, "****")
                if "Re-enter new password:" in output:
                    output = ssh.send_command_timing(new_pass, read_timeout=1)
                    print(output)
                    while True:
                        if "root@" not in output:
                            output = ssh.read_until_pattern(f'{prompt}', read_timeout=0)
                            print("Wait, the password will change now")
                            ssh.write_channel(" ")
                        elif "root@" in output:
                            print("New pass OK")
                            break

        return output
    except (NetmikoAuthenticationException, NetmikoTimeoutException) as error:
        print("*" * 5, "Error connection to:", device['host'], "*" * 5)



if __name__== "__main__":

    with open("BM10_LTE.yaml") as f:
        device = yaml.safe_load(f)
        for dev in device:
                cfg_pass(dev, commands="passwd")
