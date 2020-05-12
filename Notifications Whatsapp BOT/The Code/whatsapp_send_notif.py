
from time import sleep
from selenium import webdriver

class WhatsappSendNotifBot():
    def __init__(self, main_driver):
        self.driver = main_driver

    def find_user(self, name):
        user = self.driver.find_element_by_xpath(
            '//span[@title = "{}"]'.format(name))
        user.click()
#div._1Plpp 
    def write_message(self, msg):
        msg_box = self.driver.find_elements_by_css_selector('div._2S1VP')
        msg_box[1].send_keys(msg)

    def type_message(self):
        send_button = self.driver.find_element_by_class_name('_35EW6')
        send_button.click()
