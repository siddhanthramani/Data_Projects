import sqlite3

conn = sqlite3.connect('notifs.sqlite')
cur = conn.cursor()


def create_new_table():
    cur = conn.cursor()
    cur.execute('DROP table if exists notifs')
    cur.execute('''Create table notifs(
                notif_id   INTEGER NOT NULL 
                PRIMARY KEY AUTOINCREMENT UNIQUE
                ,contact_name TEXT
                ,called_datetime TEXT
                ,notif_datetime TEXT
                ,time_left REAL
                ,message TEXT
                ,sent INTEGER )           
                ''')
    # in reality contact id whould be the foreign key. Not contact name as it is not unique.
    # cur.execute('''Create table contacts (
    #            contact_id longint(),
    #            contact_name
    #            )''')
    conn.commit()
    cur.close()
