import sqlite3
import csv

conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()


with conn:
    c.execute("""SELECT * FROM myapp_orderpending WHERE user_id=2""")
    data = c.fetchall()
    #print(data)
    # data = [ (2,'Apple',20),() ]
    for d in data:
        print(d)
        print('-----')

########Export to CSV########
with open('allorder_user2.csv','w',newline='',encoding='utf-8') as f:
    fw = csv.writer(f) #File writer
    fw.writerows(data)