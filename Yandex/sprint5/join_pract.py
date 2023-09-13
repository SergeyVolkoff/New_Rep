import sqlite3
con = sqlite3.connect('db_video_type_slogan.sqlite')
cur = con.cursor()
results = cur.execute('''
    SELECT *
    FROM video_products, 
         slogans;
''')
for result in results:
    print(result)

con.close()