from selenium import webdriver
from time import sleep
from interact_with_user import user_lat, user_long

class StarBot_forhorizontal :

    def __init__ (self):
        self.driver = webdriver.Chrome

    def get_hori