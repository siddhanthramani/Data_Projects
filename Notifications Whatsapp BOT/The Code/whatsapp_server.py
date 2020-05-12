
import sqlite3

conn = sqlite3.connect('notifs.sqlite')
cur = conn.cursor()


def get_details():
    conn1 = sqlite3.connect('notifs.sqlite')
    cur1 = conn1.cursor()
    time_threshold = (10/(3600*24))
    print(time_threshold)
    details_obj = cur1.execute(
        '''Select notif_id, contact_name, message from notifs where time_left < (?)''', (time_threshold, ))
    details_tup_list = details_obj.fetchall()
    names = []
    messages = []
    id = []
    for details_tup in details_tup_list:
        id.append(details_tup[0])
        names.append(details_tup[1])
        messages.append(details_tup[2])

    print(id)

    # this should actually be only after the message gas been sent. Here we are doing before
    for id_val in id:
        cur1.execute('Delete from notifs where notif_id = (?)', (id_val, ))

    print(''' Sent messages have been deleted from server ''')
    conn1.commit()
    cur1.close()
    return(names, messages)


def when_next_check():
    conn2 = sqlite3.connect('notifs.sqlite')   
    cur = conn2.cursor()
    id_obj = cur.execute('''Select notif_id from notifs''')
    id_tup_list = id_obj.fetchall()
    for id_tuple in id_tup_list:
        cur.execute('''Update notifs set time_left = (SELECT julianday(notif_datetime) - julianday('now','localtime')) 
                    where notif_id = (?)''', id_tuple)

    conn2.commit()

    tl_tup_list = cur.execute('''Select time_left from notifs''')
    val_list = []

    for val in tl_tup_list:
        val_list.append(val[0])

    if not val_list:
        print('List is empty')
        cur.close()
        return 1
    else:

        print(''' When next check has executed.The actual min is ''')
        print(min(val_list))
        cur.close()
        return(min(val_list))


def add_new_row(contact_name, notif_datetime, message):
    cur = conn.cursor()
    sent = 0
    called_datetime_command = cur.execute('''
        SELECT datetime('now','localtime')
        ''')
    print(str(notif_datetime))
    called_datetime = called_datetime_command.fetchone()[0]
    time_left_command = cur.execute('''
                        SELECT julianday(?) - julianday('now','localtime')
                        ''', (notif_datetime, ))
    time_left = time_left_command.fetchone()[0]

    print(contact_name)
    print(called_datetime)
    print(notif_datetime)
    print(time_left)
    print(message)
    print(sent)

    if(time_left < 0):
        print("the time has already passed")
        cur.close()
    else:
        cur.execute('''
        Insert into notifs (contact_name, called_datetime, notif_datetime, time_left, message, sent) 
        values (?, ?, ?, ?, ?, ?)
        ''', (contact_name, called_datetime, notif_datetime, time_left, message, sent))

        print(''' Values have been inserted and commited ''')
        conn.commit()
        cur.close()
