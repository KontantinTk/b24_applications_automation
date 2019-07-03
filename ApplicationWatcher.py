from selenium import webdriver

import time

class ApplicationWatcher:

    __options = None
    __driver = None
    __path_to_driver = "C:\\tools\\chromedriver.exe"

    __state = "initial"

    __contants = {
        "path_to_portal": "https://portal.consult-info.ru/",
        "path_to_app": "https://portal.consult-info.ru/marketplace/app/7/",
        "input_login_name": "USER_LOGIN",
        "input_password_name": "USER_PASSWORD",
    }

    def __init__(self):
        print("Start watcher")
        self.__init_driver()
        self.openPortal()
        self.loginInPortal()
        self.openApp()
        self.selectAppFrame()
        self.filterByB24()
        self.refreshList()
        self.selectPortals()
        self.getList()

    def getDriver(self):
        return self.__get_driver()

    def openPortal(self):
        self.if_state("initial")
        self.__get_driver().get(self.__contants["path_to_portal"])
        self.__state = "on_auth_page"

    def loginInPortal(self):
        login, password = self.getLoginData()

        self.if_state("on_auth_page")

        login_input = self.__driver.find_element_by_name(self.__contants["input_login_name"])
        login_input.send_keys(login)

        password_input = self.__driver.find_element_by_name(self.__contants["input_password_name"])
        password_input.send_keys(password)

        submit_button = self.__driver.find_element_by_css_selector("input[type=submit]")
        submit_button.click()

        self.__state = "in_portal"

    def openApp(self):
        self.if_state("in_portal")
        self.__get_driver().get(self.__contants["path_to_app"])
        self.__state = "in_app"

    def selectAppFrame(self):
        self.if_state("in_app")
        self.__get_driver().switch_to_frame(1)
        self.__get_driver().switch_to_frame("partner_application")
        self.__state = "in_frame"

    def filterByB24(self):
        self.if_state("in_frame")
        time.sleep(6)
        self.__get_driver().find_element_by_css_selector("input[name=FIND]").click()

        time.sleep(2)
        self.__get_driver().find_element_by_css_selector(".main-ui-control.main-ui-select").click()
        time.sleep(2)

        self.__get_driver().execute_script('''
        frameElement.contentDocument.querySelector(
            "[data-type=SELECT][data-name=PARTNERSHIP] > [data-name=PARTNERSHIP]"
        ).setAttribute(
            'data-value', 
            '{"NAME":"Битрикс24","VALUE":"B24"}'
        );
        ''')

        self.__get_driver().find_element_by_css_selector("button.main-ui-filter-find").click()

    def refreshList(self, times=1):
        self.if_state("in_frame")
        time.sleep(2)
        while times > 0 or times < 0:
            time.sleep(5)
            self.if_state("in_frame")
            self.__get_driver().execute_script('''
            frameElement.contentDocument.getElementsByClassName("main-ui-search")[0].click();
            ''')
            
            if times > 0:
                times -= 1

    def selectB24(self):
        self.if_state("in_frame")
        time.sleep(2)
        self.__get_driver().execute_script('''
        frameElement.contentDocument.querySelector('[data-type=filter][data-indicator=B24]').click();
        ''')
    
    def selectPortals(self):
        self.if_state("in_frame")
        time.sleep(2)
        self.__get_driver().execute_script('''
        frameElement.contentDocument.querySelector('[data-type=filter][data-indicator=PORTALS]').click();
        ''')

    def getList(self):
        self.if_state("in_frame")
        time.sleep(2)
        
        table_list = self.__get_driver().find_elements_by_css_selector('#b24_partner_application_table tbody tr td:nth-child(2)')
        for element in table_list:
            print("innerText is " + element.get_attribute("innerText")) 

        table_list = self.__get_driver().find_elements_by_css_selector('#b24_partner_application_table tbody tr td:nth-child(4)')
        for element in table_list:
            print("innerText is " + element.get_attribute("innerText")) 
 

    #TOOLS

    def if_state(self, state):
        if self.__state == state:
            return
        else:
            print("State is not " + state + ", but " + self.__state + " is set instead!")
            self.closeBrowser()


    def getLoginData(self):
        file_name = "login_data.txt"

        fh = open(file_name, "r")

        login = fh.readline()
        password = fh.readline()

        fh.close()

        return login, password

    def closeBrowser(self):
        self.__get_driver().close()
        exit()

    def runWithDelay(self, delay_in_seconds, function):
        time.sleep(delay_in_seconds)
        function()

    #INITIALIZATION  

    def __get_driver(self):
        if self.__driver:
            return self.__driver
        else:
            self.__init_driver()

    def __get_options(self):
        if self.__driver:
            return self.__options
        else:
            self.__init_options()

    def __init_driver(self):
        self.__driver = webdriver.Chrome(
            executable_path=self.__path_to_driver, 
            chrome_options=self.__get_options())

        return self.__driver

    def __init_options(self):
        self.__options = webdriver.ChromeOptions()
        # self.__options.add_argument("headless")
        # self.__options.add_argument('window-size=900x900')

        return self.__options

        
        