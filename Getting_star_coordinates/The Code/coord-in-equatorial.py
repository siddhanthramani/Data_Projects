from selenium import webdriver
from time import sleep

from interact_with_user import username, password, starname as star_name



class StarBot_forequatorial():
    def __init__(self):
        self.driver = webdriver.Chrome()
    def search_for_star(self):
        self.driver.get("https://wikipedia.org")    
        sleep(3) 

        search_input = self.driver.find_element_by_xpath('//*[@id="searchInput"]')
        search_input.send_keys(star_name)
        
        search_button = self.driver.find_element_by_xpath('//*[@id="search-form"]/fieldset/button')
        search_button.click()

        sleep(3)
    def equatorial_param(self):
        self.right_ascension = self.driver.find_element_by_xpath('//*[@id="mw-content-text"]/div/table/tbody/tr[5]/td').text
        self.declination =  self.driver.find_element_by_xpath('//*[@id="mw-content-text"]/div/table/tbody/tr[6]/td').text


bot = StarBot_forequatorial()
bot.search_for_star()
bot.equatorial_param()

print(bot.right_ascension)
print(bot.declination)
print("Hello")
