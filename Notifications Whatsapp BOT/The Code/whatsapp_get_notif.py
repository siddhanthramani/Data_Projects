from whatsapp_server import add_new_row
from whatsapp_send_notif import WhatsappSendNotifBot
from time import sleep
from selenium import webdriver
import importlib
import datetime
import sqlite3

addednewrow = 0



class WhatsappGetNotifBot():
    # def __init__(self):
    #    self.driver = webdriver.Chrome()
    #    self.driver.get('https://web.whatsapp.com')
    #    sleep(3)
    #    input('Click button to continue')
    def __init__(self, main_driver):
        self.driver = main_driver
        self.sendbot_get = WhatsappSendNotifBot(main_driver)

    def send_message_get(self, customer_name_get, message_get):
        self.sendbot_get.find_user(customer_name_get)
        print(message_get)
        
        for i in range(0, len(message_get)):
            self.sendbot_get.write_message(message_get[i].strip())
            if message_get[i] == '':
                self.sendbot_get.type_message()

        self.sendbot_get.type_message()

        #print("typed message")


    # 

    def find_format(self, msg):
        print('Find format has been called. ')
        ret_chat = []
        
        msg_format = msg.lower().strip()
        hi_messages = ['hi', 'hello', 'helo', 'what do you do']
        
        for check in hi_messages:
            if check == msg_format : 
                ret_status = 1
                ret_message = '''Hello! 
                            Thanks for trying out the notifications bot.\b
                            If you ever want a reminder or important notification to be delivered on  
                            time while not getting lost in a deluge of notifications,we are here to help  
                            you.
                            \n\nAs we are in our beta version, to provide a good service, please keep the
                            following points in mind when you keep a remainder.
                            \n\n1. The first line should have the following format.                 
                                on 21st April @11:45
                                It should have the on and @ symbols at the respective places.
                                The spaces between on and day , day and month is a must.
                                The month should be in words
                                The time should immediately follow the @symbol
                                The time should be in 24hr format
                            2.You must press enter after the first line.  
                            3.From the second line, you can type your remainder in less than
                            50 words. This is to help us prevent spam.
                            We will roll out more user friendly options later in our updates.
                            \n\nPin us to the top of your whatsapp chat and enable notifications to ensure that
                            you dont miss your reminders.
                            Thanks for choosing us. Have a great day :)'''

                            
                ret_chat = ret_message.split('\n')
                break
            else:
                ret_status = 0
                ret_chat = '' 

        return (ret_status, ret_chat)

    def find_notifs_datetime(self, msg):

        month_in_number = {'january': '1',
                           'february': '2',
                           'march': '3',
                           'april': '4',
                           'may': '5',
                           'june': '6',
                           'july': '7',
                           'august': '8',
                           'september': '9',
                           'october': '10',
                           'november': '11',
                           'december': '12',
                           }

        first_line = msg.split('\n')[0].lower()

        let_at = str(first_line).find('at')
        let_a = str(first_line).find('@')
        let_on = str(first_line).find('on')
        if (let_a == -1 and let_at == -1) or let_on == -1 or ((let_a - let_on) < 0 and (let_at - let_on) < 0 ) :
            print("Error in format : on or @")
            return 0
        # to get the date

        
        if let_a != -1:
            notif_datetime = first_line.split('on')[1].split('@')
        elif let_at != -1:
            notif_datetime = first_line.split('on')[1].split('at')    
        notif_date = notif_datetime[0].strip().split()

        # to get the day
        # this assumes st, rd, th would be written
        n_day = notif_date[0]
        if(len(n_day) == 3):
            notif_day = n_day[0:1]
        elif (len(n_day) == 4):
            notif_day = n_day[0:2]
        elif (len(n_day) == 2 or len(n_day) == 1):
            notif_day = n_day
        else:
            print('Error in format : Day')
            print(len(n_day))
            print(n_day)
            print(notif_date)
            print(notif_datetime)
            return 0

        # to get the month
        n_date = notif_date[1].strip()
        notif_date = n_date.lower()
        notif_date_no = month_in_number[notif_date]

        # to get the year(assuming date of notif is on the same year)
        notif_year = datetime.datetime.now().year

        # to get the time
        notif_time = notif_datetime[1].strip()
        notif_hr = notif_time.split(':')[0]
        notif_min = notif_time.split(':')[1]

        notif_date_time = datetime.datetime(
            int(notif_year),
            int(notif_date_no),
            int(notif_day),
            int(notif_hr),
            int(notif_min),
            0
        )
        return notif_date_time

    def find_notifs_message(self, msg):
        first_line = msg.split('\n')[0]
        message = msg[len(first_line):len(msg)]
        print(message)
        return message

    def getmessage(self, noofmsg, name_of_cust):
        print(''' get message has been called ''')
        msgs = self.driver.find_elements_by_css_selector(
            'div._3zb-j span span')
        totalno = len(msgs)
        print(''' Received the new messages of the user ''')
        for i in range(totalno-noofmsg, totalno):
            notif_datetime = self.find_notifs_datetime(msgs[i].text)
            print(''' Found required datetime ''')
            
            (ret_status, ret_chat) = self.find_format(msgs[i].text)
            
            if ret_status == 1:
                print('ret_status is 1. ')
                self.send_message_get(name_of_cust, ret_chat)
                continue
                
            if(notif_datetime == 0):
                continue

            print(msgs[i].text)
            the_message = self.find_notifs_message(msgs[i].text)
            if len(the_message.split()) >= 50:
                continue
            print(''' found the message ''')
            print(''' Called the add new row function ''')
            #.replace('\n', '\t')
            add_new_row(name_of_cust, notif_datetime, the_message)

    def find_new_user_messages(self):
        print(''' find_new_user_messages has been called ''')
        list_new_messages = self.driver.find_elements_by_xpath(
            '//span[@class = "OUeyt"]/parent::*/parent::*/parent::*/parent::*')

        no_of_new_messages_list = self.driver.find_elements_by_xpath(
            '//span[@class = "OUeyt"]')

        if len(list_new_messages) <= 0:
            print('No new notifs. ')
            return len(list_new_messages)

        for i in range(0, len(list_new_messages)):

            no_of_new_messages = int(no_of_new_messages_list[i].text)
            # the top part should be before the below part, otherwise throws exception
            list_new_messages[i].click()
            print(''' Clicked on the user request ''')
            sleep(5)

            name_of_cust_list = self.driver.find_elements_by_css_selector(
                'div._5SiUq div div span._1wjpf')
            name_of_cust = name_of_cust_list[i].text
            print(''' Received name of the user  ''')
            self.getmessage(no_of_new_messages, name_of_cust)

        return len(list_new_messages)
        #list_new_messages = self.driver.find_elements_by_class_name('OUeyt')
        # for i in range(1, len(list_new_messages), 1):
        #    if list_new_messages[i].text > 0 :
        #        find_new_user_messages
        #        getmessage(list_new_messages[i])
