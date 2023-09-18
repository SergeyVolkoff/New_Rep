import sqlite3
con = sqlite3.connect('db_video_type_slogan.sqlite')
cur = con.cursor()
results = cur.execute('''
    SELECT video_products.title,
       slogans.slogan_text
FROM video_products
FULL JOIN slogans ON video_products.slogan_id = slogans.id;  
''')
for result in results:
    print(result)

con.close()