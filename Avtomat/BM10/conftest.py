"""
Файл предназначен для вставки коомента в тест!

"""
#from rich import print
import time

def pytest_report_header(config):
        print ("\33[31m{}".format("Для теста <<test_workSTP>> нужно сделать кольцо или избыточный линк на 3 и 4 портах.\n"
                                  "Осталось 10 сек!"))
        spinner = '|/-\|/-\|/-\|/-\|/-\|/-\|/-\|'
        for i in spinner:
            print(f"\r{i}",end = "", flush = True)
            time.sleep(0.3)