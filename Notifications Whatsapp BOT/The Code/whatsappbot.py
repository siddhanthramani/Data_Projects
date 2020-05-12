from selenium import webdriver

driver = webdriver.Chrome()
driver.get('https://web.whatsapp.com')

name = input('Enter the name of the person or group : ')
msg = input('Enter the message to be sent : ')




class WhatsappSendNotifBot(self){

    void find_user(self, name){
        user = self.driver.find_element_by_xpath('//span[@title = "{}"]'.format(name))
        user.click()
    }

    void send_message(self, msg){
        msg_box = self.driver.find_element_by_class_name('_39LWd')
        msg_box.send_keys(msg)

        send_button = self.driver.find_element_by_class_name('_35EW6')
        send_button.click()


    }

}

sendbot = WhatsappSendNotifBot()
sendbot.find_user(name)
sendbot.send_message(msg)