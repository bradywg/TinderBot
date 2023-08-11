from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
import openai
import random
from Read_gamilV2 import get_2fa_code_from_gmail
import os
from selenium.common.exceptions import StaleElementReferenceException
import time

from config import phone


Gmail_key="ENTER YOUR GMAIL KEY HERE"
#openapi_key= api_key

class Bot():
    def __init__(self):
        path = os.path.dirname(os.path.abspath(__file__))
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(
        os.path.join(path, 'chromedriver'),
        chrome_options=chrome_options)

    def open_tinder(self):
        sleep(2)
        self.driver.get('https://tinder.com/app/explore')
        login_button = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "Log in")]')))
        login_button.click()
        sleep(5) 
        self.login_phone() 
        try:
            allow_location_button = self.driver.find_element('xpath', '//*[@id="t-1917074667"]/main/div/div/div/div[3]/button[1]')
            allow_location_button.click()
        except:
            print('no location popup')

        try:
            notifications_button = self.driver.find_element('xpath', '/html/body/div[2]/main/div/div/div/div[3]/button[2]')
            notifications_button.click()
        except:
            print('no notification popup')
        
    def like(self):
        sleep(5)
        body = self.driver.find_element('xpath', '//*[@id="Tinder"]/body')
        body.send_keys(Keys.ARROW_RIGHT)

    def nope(self):
        sleep(5)
        body = self.driver.find_element('xpath', '//*[@id="Tinder"]/body')
        body.send_keys(Keys.ARROW_LEFT)

    def check(self):
        Ready = input("Are you logged in?" )
        if(Ready):
            body = self.driver.find_element('xpath', '//*[@id="Tinder"]/body')
            for x in range(8):
                sleep(2)
                body.send_keys(Keys.SPACE)
        else:
            sleep(5)

    def login_phone(self):
        login_with_Phone=WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH,'//div[contains(text(), "Log in with phone number")]')))
        login_with_Phone.click()
        sleep(30)
        phone_wait=WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, 'phone_number')))
        phone_form=self.driver.find_element(By.NAME,'phone_number')
        phone_form.send_keys(phone)
        cont=WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH,'//div[contains(text(), "Continue")]')))
        cont.click()
        sleep(15)
        phone_two_fa=get_2fa_code_from_gmail("New text message")
        print(phone_two_fa)
        phone_fa=self.driver.find_element(By.XPATH,'//*[@id="u-1238065328"]/main/div[1]/div[1]/div/div[3]/div/div[1]/div[2]/input') 
        phone_fa.send_keys(phone_two_fa)
        cont=WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH,'//div[contains(text(), "Continue")]')))
        cont.click()
        sleep(10)
        Gmail_Twofa=self.driver.find_element(By.XPATH,'//*[@id="u-1238065328"]/main/div[1]/div/div[1]/div/div[2]/div[1]/div[2]/div/div[1]/div[2]/input')
        Gmail_two_fa=get_2fa_code_from_gmail("Let’s get you verified")
        print(Gmail_two_fa)
        Gmail_Twofa.send_keys(Gmail_two_fa)
        cont=WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH,'//div[contains(text(), "Confirm email")]')))
        cont.click()
        sleep(2)


        
bot=Bot()
bot.open_tinder()
bot.check()


