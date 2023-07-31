import re
import yaml
import netmiko
import pytest
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)
from clss_Router import Router
from check_workSTP import  check_workSTP


def pytest_report_header(config):  # pytest_report_header спец конструкция!!!

    print(
        "\33[31m{}".format("Для теста <<test_workSTP>> нужно подготовить кольцо или избыточный линк на 3 и 4 портах.\n"
                           "Осталось 10 сек!/n"))
    print("\33[33m{}".format("Кабель вставить в порт сразу ПОСЛЕ появления 'test_check_workSTP' "))
    spinner = '|/-\|/-\|/-\|/-\|/-\|/-\|/-\|'  # вставляем спиннер на 10 сек
    for i in spinner:
        print(f"\r{i}", end="", flush=True)
        time.sleep(0.4)
def test_base_cfg():
    assert check_workSTP("logread -l 10")==True, "STP is not work"


