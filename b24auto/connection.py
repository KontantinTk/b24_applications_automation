from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

from b24auto.constants import Messages, B24, Settings


class B24Connection:
    screenshots_folder = '/home/b24_applications_automation/screenshots/'
    path_to_driver = "/home/b24_applications_automation/files/chromedriver"

    def __init__(self):
        print(Messages.start_app_message)

    def test(self):
        browser = self.__get_browser()
        self.save_screenshot(browser)

    def save_screenshot(self, browser, file_name="test.png"):
        browser.save_screenshot(self.screenshots_folder + file_name)

    def __get_browser(self):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--window-size=1920x1080')

        browser = Chrome(executable_path=self.path_to_driver, chrome_options=options)
        print("Path to portal is {}".format(B24.path_to_portal))
        browser.get(B24.path_to_portal)

        return browser
