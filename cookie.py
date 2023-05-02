#from autevo import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ECz
import undetected_chromedriver as uc
from fake_useragent import UserAgent, FakeUserAgentError
import os, pickle
from os.path import exists

class Browser:    
    def __init__(self):
        
        try:
            ua = UserAgent()
            self.user_agent = ua.random
        except FakeUserAgentError:
            self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
        options = uc.ChromeOptions()
        #options = ChromeOptions()
        options.add_argument("--start-maximized")
        #options.add_argument("--headless")
        options.add_argument('--no-sandbox')   
        options.add_argument('--disable-dev-shm-usage')   
        
        # options.add_argument("--user-agent=" + self.user_agent)
        self.bot = uc.Chrome(options=options, use_subprocess=True)
        self.bot.delete_all_cookies()
        
    def getBot(self):
        return self.bot 

class Cookies:
    def __init__(self, bot):
        self.bot = bot
        self.cookies_dir = os.path.join(os.getcwd(), "CookiesDir")
        if not exists(self.cookies_dir):
            os.mkdir(self.cookies_dir)
        self.selectCookie()


    def selectCookie(self):
        if len(os.listdir(self.cookies_dir)) > 0:
            print("Select Cookie number that you want to use:: ")
            cookies_dict = dict(enumerate(os.listdir(self.cookies_dir)))
            for index, filename in enumerate(os.listdir(self.cookies_dir)):
                print(f"({index}) --> {filename}")
            print("(a) --> Add NEW Cookie.")
            selected = 0
            while type(selected) is not int or not 0 <= selected < len(os.listdir(self.cookies_dir)):
                try:
                    selection = input("Please select an integer representing a cookie::")
                    selected = int(selection)
                except ValueError:
                    if selection == "a":
                        self.createCookie()
                        return
                    pass

            selected_cookie = cookies_dict[selected]
            self.loadCookies(selected_cookie)
            print("loadCookies stored on save directory!")
        else:
            print("No cookies stored on save directory!")
            self.createCookie()


    def loadCookies(self, selected_cookie):
        # Using chrome, sameSite cookie must not be set to None due to Google's policy.
        cookie_path = os.path.join(self.cookies_dir, selected_cookie)
        cookie_data = pickle.load(open(cookie_path, "rb"))
        for cookie in cookie_data:
            if 'sameSite' in cookie:
                if cookie['sameSite'] == 'None':
                    cookie['sameSite'] = 'Strict'
            self.bot.add_cookie(cookie)


    def createCookie(self):
        print("Your browser currently shows the tiktok login page, please login in.")
        input("After you have logged in fully, please press any button to continue...")
        print("#####")
        filename = input("Please enter a name for the cookie to be stored as::: ")
        cookie_path = os.path.join(self.cookies_dir, filename+".cookie")
        pickle.dump(self.bot.get_cookies(), open(cookie_path, "wb+"))
        print("Cookie has been created successfully, resuming upload!")     
