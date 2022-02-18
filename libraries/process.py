from libraries.common import log_message, capture_page_screenshot, browser
from libraries.mundialitis.mundialitis import Mundialitis
from config import OUTPUT_FOLDER


class Process:
    def __init__(self, credentials: dict):
        log_message("Initialization")
        prefs = {
            "profile.default_content_setting_values.notifications": 2,
            "profile.default_content_settings.popups": 0,
            "directory_upgrade": True,
            "download.default_directory": OUTPUT_FOLDER,
            "plugins.always_open_pdf_externally": True,
            "download.prompt_for_download": False
        }
        browser.open_available_browser(preferences = prefs)
        browser.set_window_size(1920, 1080)
        browser.maximize_browser_window()
        mundialitis = Mundialitis(browser, credentials["Mundialitis"])
        mundialitis.login()
        self.mundialitis = mundialitis


    def start(self):
        log_message("Start - Create Lobby")
        self.mundialitis.create_lobby()
        log_message("End - Create Lobby")
        log_message("Start - Register New User")
        self.mundialitis.register_new_user()
        log_message("Finish - Register New User")
        log_message("Start - Join Lobby")
        self.mundialitis.join_lobby("user")
        log_message("Finish - Join Lobby")
        log_message("Start - Login with First User")
        self.mundialitis.login()
        log_message("Finish - Login with First User")
        log_message("Start - Join Lobby with First User")
        self.mundialitis.join_lobby("creator")
        log_message("Finish - Join Lobby with First User")
        log_message("Start - Start Game")
        self.mundialitis.start_game()
        log_message("Finish - Start Game")
        log_message("Start - Play Game")
        self.mundialitis.play_game()
        log_message("Finish - Play Game")


    def finish(self):
        log_message("DW Process Finished")
        browser.close_browser()