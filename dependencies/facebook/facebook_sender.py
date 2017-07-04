import logging as LOGGER
from facebook_ui import FacebookUI, firefox

class SeleniumSender:
    def __init__(self, fb_login=None, fb_password=None, driver=None):
        LOGGER.debug("Initializing Selenium driver...")
        self.session = FacebookUI({'firefox': firefox})
        LOGGER.debug("Facebook Log in...")
        self.session.do_login(fb_login, fb_password)

    def send_private_message(self, page_id, message):
        LOGGER.debug("Facebook: private message on page %s %s" % (page_id, message))
        self.session.write_to_chat(page_id, message)

    def attach_image_private_message(self, page_id, img_name):
        LOGGER.debug("Facebook: private message on page %s %s" % (page_id, img_name))
        self.session.attach_image_to_chat(page_id, img_name)

    def clickSend(self):
        self.session.click_send()

    def teardown(self):
        self.session.teardown()
