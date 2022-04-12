"""
Задание 7.1

Обработать строки из файла ospf.txt и вывести информацию по каждой строке в таком
виде на стандартный поток вывода:

Prefix                10.0.24.0/24
AD/Metric             110/41
Next-Hop              10.0.13.3
Last update           3d18h
Outbound Interface    FastEthernet0/0

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""

result = "\n{:25}{}"*5
with open("ospf.txt", "r") as f:
    for line in f:
        line = line.replace("[","").replace("]", "").replace(",", "").replace("via", "")

        line = line.split()


        print (result.format(
        "Prefix", line[1],
        "AD/Metric", line[2],
        "Next-Hop", line[3],
        "Last update", line[4],
        "Outbound Interface", line[5]
        ))

