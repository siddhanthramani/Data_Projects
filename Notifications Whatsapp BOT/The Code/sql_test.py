
import sqlite3

conn = sqlite3.connect('notifs.sqlite')
cur = conn.cursor()
notif_datetime = '2020-04-22 17:56:00'
time_left_command = cur.execute('''
                        SELECT julianday(?) - julianday('now','localtime')
                        ''', (notif_datetime, ))
timeleft = time_left_command.fetchone()[0]

cur.execute('''
        Insert into notifs (contact_name, called_datetime, notif_datetime, time_left, message, sent) 
        values (?, ?, ?, ?, ?, ?)
        ''', ('Amma', '2020-04-22 18:16:00', '2020-05-22 18:16:00', timeleft, "message", 0))
conn.commit()
print(timeleft)
