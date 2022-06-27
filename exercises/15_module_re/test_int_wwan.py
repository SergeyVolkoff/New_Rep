# Создать функцию для настройки и проверки интерфейса wwan0.

import pexpect


def send_show_ifcof(ip, user, password, commanda):
    print(f"Connect to {ip}")
    try:
        with pexpect.spawn(f"ssh {user}@{ip}", timeout=10, encoding="utf-8") as ssh:
            ssh.expect("d:")

            ssh.sendline(password)
            ssh.expect("root@BWOS:~#")

            ssh.sendline(commanda)
            ssh.expect("root@BWOS:~#")
            output = ssh.before
            return output
    except pexpect.exeptions.TIMEOUT as error:
        print(f"error connect tp {ip}")

if __name__=="__main__":
    print(send_show_ifcof("192.168.2.1", "root", "128500", "ifconfig"))
