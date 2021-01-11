import sqlite3
import csv

conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()

def wrietodb(token,approved,user_id):
    ID = None
    # write data to verifyemail table
    with conn:
        c.execute("""INSERT INTO myapp_verifyemail VALUES (?,?,?,?)""",
        (ID,token,approved,user_id))
    conn.commit()#save to database
    print('Complete')


#writodb('asfsddfgsdfhdsh',1,3)


########Read CSV########
with open('newtoken.csv',newline='',encoding='utf-8') as f:
    fr = csv.reader(f) #File reader
    #print(list(fr))

    for tk,a,u in fr:
        wrietodb(tk,int(a),int(u))
