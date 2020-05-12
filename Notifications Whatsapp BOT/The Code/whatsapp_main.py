import re
import sqlite3
import threading
import datetime
from whatsapp_server import when_next_check, get_details
from whatsapp_send_notif import WhatsappSendNotifBot
from whatsapp_get_notif import WhatsappGetNotifBot, addednewrow

from notifs_table_creation import create_new_table
from time import sleep
from selenium import webdriver
import importlib

print(addednewrow)
create_new_table()


main_driver = webdriver.Chrome()

getbot = WhatsappGetNotifBot(main_driver)
sendbot = WhatsappSendNotifBot(main_driver)

main_driver.get('https://web.whatsapp.com')
sleep(3)
input('Click button to continue : ')


def timer_for_check():
    print('timing check has been done')
    days_left = when_next_check()
    print('Days left are, the returned value')
    print(days_left)
    print(days_left * 24 * 60)
    # timer.close()
    # 60 seconds buffer time
    #global timer
    #timer.close()

    seconds_left = days_left * 24 * 3600
    timer = threading.Timer(seconds_left, send_notif)
    timer.start()
    
    

def send_notif():
    names = []
    messages = []
    (names, messages) = get_details()
    print('Going to send notif')
    

    for i in range(0, len(names)):
        print(names[i])
        print(messages[i])
        sendbot.find_user(names[i])
        print('found user')
        sendbot.write_message(messages[i])
        print('Message written')
        sendbot.type_message()
        print('Message has been sent')
    timer_for_check()


while(1):
    any_message = getbot.find_new_user_messages()
    if any_message > 0:
        timer_for_check()
    # after every 10 second notif check, if any new row is added. then goes checks
    # in reality we need to compare only last min time left(current time) and new time left
    sleep(5)
