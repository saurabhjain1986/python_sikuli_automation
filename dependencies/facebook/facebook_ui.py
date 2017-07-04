import os
import signal
import time
import traceback
from argparse import ArgumentParser


from org.openqa.selenium import WebDriver, By, Keys
from org.openqa.selenium.firefox import FirefoxDriver
from org.openqa.selenium.support.ui import WebDriverWait
from org.openqa.selenium.support.ui import ExpectedConditions as EC
from org.openqa.selenium.interactions import Actions as AC
from org.openqa.selenium.remote import DesiredCapabilities

import wde


FB_URL = 'https://m.facebook.com'


def retry(fn, times=3, sleep_on_error=1):
    i = 0
    while i < times:
        try:
            return fn()
        except:
            print("Attempt #%s" % (i + 1))
            traceback.print_exc()
            time.sleep(sleep_on_error)
        i += 1
    raise RuntimeError("Failed to return result %s times" % times)

def firefox():
    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.startup.homepage", "about:blank")
    profile.set_preference("startup.homepage_welcome_url", "about:blank")
    profile.set_preference("startup.homepage_welcome_url.additional", "about:blank")
    return retry(lambda: webdriver.Firefox())


def try_or_teardown(method):
    def _wrapped(self, *args, **kwargs):
        try:
            return method(self, *args, **kwargs)
        except:
            self.teardown()
            raise
    return _wrapped


class FacebookUI(object):
    def __init__(self, driver):
        self.driver = FirefoxDriver()
        self.driver.manage().window().maximize()
        self.wait = WebDriverWait(self.driver, 30)

    def _dump_page(self, filename):
        import time
        try:
            self.driver.save_screenshot('screen_%s.png' % time.time())
            # time.sleep(5)
            # print '\n\t\t\tBEGIN %s\n' % filename
            # print self.driver.page_source
            # print '\n\t\t\tEND %s\n' % filename
        except:
            pass

    @try_or_teardown
    def do_login(self, login, password):
        self.driver.get(FB_URL)

        login_field = self.wait.until(EC.presenceOfElementLocated((By.name('email'))))
        login_field.sendKeys(login)

        password_field = self.wait.until(EC.presenceOfElementLocated((By.name('pass'))))
        password_field.sendKeys(password)

        login_button_locator = "//input[@name='login']"
        login_button = self.wait.until(EC.elementToBeClickable(By.xpath(login_button_locator)))
        login_button.click()

        notNow_button_locator = "//a[span[text()='Not Now']]"
        if self.driver.findElements(By.xpath(notNow_button_locator)).size() > 0:
            notNow_button = self.wait.until(EC.presenceOfElementLocated(By.xpath(notNow_button_locator)))
            notNow_button.click()


        self.wait.until(EC.presenceOfElementLocated((By.xpath("//*[text()='Home']"))))

    @try_or_teardown
    def post_message(self, url, message):
        url = self._prepare_url(url)
        self.driver.get(url)
        message_field_xpath = "//*[@name='xhpc_message_text']"  # textarea 'Write somthing on this page...'
        message_field = self.wait.until(EC.presenceOfElementLocated((By.xpath(message_field_xpath))))
        ctrl_enter = (Keys.CONTROL + Keys.ENTER)
        message_field.sendKeys(message)
        publish_btn = self.wait.until(EC.elementToBeClickable(By.xpath("//*[text()='Post']")))
        publish_btn.click()
        #message_field.sendKeys(ctrl_enter)

    @try_or_teardown
    def write_to_chat(self, url, msg):
        url = self._prepare_url(url)
        self.driver.get(url)
        # new_msg_btn_locator = "//*[text()='Send Message']"
        new_msg_btn_locator = "//a[span[text()='Message']]"
        new_msg_btn = self.wait.until(EC.presenceOfElementLocated((By.xpath(new_msg_btn_locator))))
        new_msg_btn.click()
        # msg_txt_locator = '//div[@class="_5rpu" and @role="textbox"]'
        msg_txt_locator = "//textarea[@id='composerInput']"
        actions = AC(self.driver)
        msg_txt = self.wait.until(EC.elementToBeClickable((By.xpath(msg_txt_locator))))
        msg_txt.click()
        msg_txt.sendKeys(msg)
        msg_send_button_locator = "//input[@Value='Send']"
        msg_send_button = self.wait.until(EC.elementToBeClickable((By.xpath(msg_send_button_locator))))
        msg_send_button.click()

    @try_or_teardown
    def attach_image_to_chat(self, url, img_name):
        url = self._prepare_url(url)
        self.driver.get(url)
        # new_msg_btn_locator = "//*[text()='Send Message']"
        new_msg_btn_locator = "//a[span[text()='Message']]"
        new_msg_btn = self.wait.until(EC.presenceOfElementLocated((By.xpath(new_msg_btn_locator))))
        new_msg_btn.click()
        attach_image_btn_locator = "//input[@value='Add Photos']"
        attach_image_btn = self.wait.until(EC.presenceOfElementLocated((By.xpath(attach_image_btn_locator))))
        attach_image_btn.click()
        browse_btn_locator = "//input[@name='file1']"
        browse_btn = self.wait.until(EC.presenceOfElementLocated((By.xpath(browse_btn_locator))))
        browse_btn.click()
        w = wde.WDE()
        w.enterFileName(img_name)
        msg_send_button_locator = "//input[@Value='Send']"
        msg_send_button = self.wait.until(EC.elementToBeClickable((By.xpath(msg_send_button_locator))))
        msg_send_button.click()

    @try_or_teardown
    def click_send(self):
        msg_send_button_locator = "//input[@Value='Send']"
        msg_send_button = self.wait.until(EC.elementToBeClickable((By.xpath(msg_send_button_locator))))
        msg_send_button.click()

    @staticmethod
    def _prepare_url(url):
        if not url.startswith(FB_URL):
            return '{}/{}'.format(FB_URL, url)
        return url

    def teardown(self):
        driver = self.driver
        if driver is None:
            return
        driver.close()
        driver.quit()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            print exc_type, exc_val, exc_tb
        self.teardown()


if __name__ == '__main__':
    parser = ArgumentParser(description='Work with Facebook as user.')
    parser.add_argument('--login', type=str, required=True, help='email or phone number')
    parser.add_argument('--password', type=str, required=True, help='facebook password')
    parser.add_argument('--url', type=str, required=True, help='page name or id')
    parser.add_argument('--message', type=str, required=True, help='enter text to post on the page')
    parser.add_argument('--recipient', type=str, required=False, help='choose recipient for your private message')
    args = parser.parse_args()

    with FacebookUI(firefox()) as ui_session:
        ui_session.do_login(args.login, args.password)
        ui_session.write_to_chat(args.url, args.message)
