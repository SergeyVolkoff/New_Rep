 # Создать функцию для настройки и проверки интерфейса wwan0.

import pexpect
from pprint import pprint
from show_BM10 import send_show_ifcof
from cfg_wwan0_BM10 import cfg_wwan_BM10



opros=send_show_ifcof("192.168.2.1", "root", "128500")
print("_"*10, opros)
if "add" in opros:
    print("Interface has ip,\n start ping")
else:
    cfg =cfg_wwan_BM10("root", "192.168.2.1", "128500",cfg_commands)



if __name__=="__main__":
   pprint(send_show_ifcof(ip,user_name,pas))
