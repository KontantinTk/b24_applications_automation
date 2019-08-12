from selenium import webdriver

import time

from b24auto import config, constants
from b24auto.config import ConfigProvider


class ApplicationWatcher:
    __options = None
    __driver = None
    __path_to_driver = ConfigProvider.get_config()["path_to_driver"]

    __state = "initial"

    __contants = {
        "path_to_portal": constants.PATH_TO_PORTAL,
        "path_to_app": constants.PATH_TO_APP,
        "input_login_name": "USER_LOGIN",
        "input_password_name": "USER_PASSWORD",
    }

    def __init__(self):
        print("Start watcher")
        self.__init_driver()
        self.openPortal()
        self.loginInPortal()
        self.openApp()
        # self.makeScreenshow("login_form.png")
        # self.closeBrowser()

        self.selectAppFrame()

    def start(self):
        self.filterByB24()
        self.refreshList()
        self.selectPortals()
        # self.selectB24()
        self.filterByCity()
        self.getAllPortals()
        self.getErrors()
        # self.getList()

    def end(self):
        self.closeBrowser()

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
        while not self.__state == "in_frame":
            try:
                time.sleep(1)
                self.__get_driver().switch_to_frame("partner_application")
                self.__state = "in_frame"
            except:
                print('Couldnt select frame')

    def filterByB24(self):
        self.if_state("in_frame")
        time.sleep(2)
        self.__get_driver().find_element_by_css_selector("input[name=FIND]").click()

        # time.sleep(2)
        self.__get_driver().find_element_by_css_selector(
            "[data-name=PARTNERSHIP].main-ui-control.main-ui-select").click()
        # time.sleep(2)

        self.__get_driver().execute_script('''
        frameElement.contentDocument.querySelector(
            "[data-type=SELECT][data-name=PARTNERSHIP] > [data-name=PARTNERSHIP]"
        ).setAttribute(
            'data-value', 
            '{"NAME":"Битрикс24","VALUE":"B24"}'
        );
        ''')

        self.__get_driver().find_element_by_css_selector("button.main-ui-filter-find").click()

    def filterByCanGet(self):
        self.if_state("in_frame")
        time.sleep(2)
        self.__get_driver().find_element_by_css_selector("input[name=FIND]").click()

        self.__get_driver().find_element_by_css_selector(
            "[data-name=APPLICATION_BUSY].main-ui-control.main-ui-select").click()

        self.__get_driver().execute_script('''
                frameElement.contentDocument.querySelector(
                    "[data-type=SELECT][data-name=APPLICATION_BUSY] > [data-name=APPLICATION_BUSY]"
                ).setAttribute(
                    'data-value',
                    '{"NAME":"Можно взять","VALUE":"FREE"}'
                );
                ''')

        self.__get_driver().find_element_by_css_selector("button.main-ui-filter-find").click()

    def filterByCity(self, city_name='Москва'):
        self.if_state("in_frame")
        time.sleep(2)
        error = True
        while error:
            try:
                time.sleep(1)
                self.__get_driver().find_element_by_css_selector("input[name=FIND]").click()

                city_input = self.__get_driver().find_element_by_css_selector(
                    "[name=CITY].main-ui-control.main-ui-control-string")
                city_input.clear()
                city_input.send_keys(city_name)

                self.__get_driver().find_element_by_css_selector("button.main-ui-filter-find").click()
                error = False
            except:
                pass

    def refreshList(self, times=1):
        self.if_state("in_frame")
        time.sleep(1)
        while times > 0 or times < 0:
            time.sleep(1)
            self.if_state("in_frame")
            self.__get_driver().execute_script('''
            frameElement.contentDocument.getElementsByClassName("main-ui-search")[0].click();
            ''')

            if times > 0:
                times -= 1

    def selectB24(self):
        self.if_state("in_frame")
        time.sleep(1)
        self.__get_driver().execute_script('''
        frameElement.contentDocument.querySelector('[data-type=filter][data-indicator=B24]').click();
        ''')

    def selectPortals(self):
        self.if_state("in_frame")
        time.sleep(1)
        self.__get_driver().execute_script('''
        frameElement.contentDocument.querySelector('[data-type=filter][data-indicator=PORTALS]').click();
        ''')

    def getList(self):
        self.if_state("in_frame")
        time.sleep(2)

        # self.__get_driver().find_element_by_css_selector(
        #     '#menu-popup-b24_partner_application_grid_page_size_menu [data-value="20"]').click()

        table_list = self.__get_driver().find_elements_by_css_selector(
            '#b24_partner_application_table tbody tr td:nth-child(6)')

        buttons = []
        for element in table_list:
            button = element.find_element_by_css_selector(
                '.partner-application-b24-list-item-submit-link-cnr.partner-application-b24-application .js-partner-submit-application')
            buttons.append(button)

        return buttons

    # todo: checking for success
    def getAllPortals(self):
        time.sleep(2)
        error = True
        while error:
            try:
                time.sleep(1)
                self.__get_driver().find_element_by_css_selector('[data-value=GET_ALL_PORTALS]').click()
                error = False
            except:
                pass

    def getErrors(self):
        error = True
        while error:
            try:
                time.sleep(1)
                text = self.__driver. \
                    find_element_by_css_selector('.partner-application-b24-list-automatic-action-errors-item-cnr'). \
                    get_attribute('innerText')

                new_datetime_string = config.get_datetime_string_from_text(text)
                config.update_datetime_file(new_datetime_string)
                error = False
            except:
                pass

    # TOOLS

    def makeScreenshow(self, filename):
        self.__get_driver().save_screenshot(filename)

    def if_state(self, state):
        if self.__state == state:
            return
        else:
            print("State is not " + state + ", but " + self.__state + " is set instead!")
            self.closeBrowser()

    def getLoginData(self):
        login = ConfigProvider.get_config()['auth_data']['login']
        password = ConfigProvider.get_config()['auth_data']['password']

        return login, password

    def closeBrowser(self):
        self.__get_driver().close()
        exit()

    def runWithDelay(self, delay_in_seconds, function):
        time.sleep(delay_in_seconds)
        function()

    # INITIALIZATION

    def __get_driver(self):
        if self.__driver:
            return self.__driver
        else:
            self.__init_driver()

    def __init_driver(self):
        options = self.__get_options()

        self.__driver = webdriver.Chrome(
            executable_path=self.__path_to_driver,
            chrome_options=options)

        self.__driver.set_window_size(1920, 1080)

        return self.__driver

    def __get_options(self):
        if not self.__options:
            self.__init_options()

        return self.__options

    def __init_options(self):
        options = webdriver.ChromeOptions()
        for driver_option in ConfigProvider.get_config()['driver_options']:
            options.add_argument(driver_option)

        self.__options = options
        return options
