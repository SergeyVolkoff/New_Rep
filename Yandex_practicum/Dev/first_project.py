from prettytable import PrettyTable

table = PrettyTable()

table.field_names = ['Name', 'Age', 'City']
table.add_row(['Стёпа', 11, 'Москва'])
table.add_row(['Андрей', 7, 'Ковров'])
table.add_row(['Тоня', 6, 'Минск'])
table.add_row(['Толя', 8, 'Санкт-Петербург'])
table.add_row(['Лера', 5, 'Краснодар'])

print(table) 