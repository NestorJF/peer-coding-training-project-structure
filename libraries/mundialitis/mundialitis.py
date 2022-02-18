from libraries.common import act_on_element, capture_page_screenshot, log_message
from config import OUTPUT_FOLDER
import random

class Mundialitis():

    def __init__(self, rpa_selenium_instance, credentials: dict):
        self.browser = rpa_selenium_instance
        self.mundialitis_url = credentials["url"]
        self.mundialitis_login = credentials["login"]
        self.mundialitis_password = credentials["password"]
        self.lobby = ""

    def login(self):
        """
        Login to Mundialitis with Bitwarden credentials.
        """
        try:
            self.browser.go_to(self.mundialitis_url)
            self.input_credentials()
            self.submit_form()
        except Exception as e:
            capture_page_screenshot(OUTPUT_FOLDER, "Exception_Mundialitis_Login")
            raise Exception("Login to Mundialitis failed")


    def input_credentials(self):
        """
        Function that writes the credentials in the login form.
        """
        self.browser.click_element('//a[text()="LOGIN"]')
        self.browser.input_text_when_element_is_visible('//input[@id="logusername"]', self.mundialitis_login)
        self.browser.input_text_when_element_is_visible('//input[@id="logpassword"]', self.mundialitis_password)
        return

    def submit_form(self):
        """
        Function that submits the login form and waits for the main page to load.
        """
        self.browser.click_element('//button[@name="login"]')
        act_on_element('//div[@id="main"]', "find_element")
        return
    
    def create_lobby(self):
        """
        Creates a new lobby for the trivia page.
        """
        new_lobby = "RPALOBBYN12"
        act_on_element('//a[@href="/trivialobbies"]', "click_element")
        act_on_element('//button[text()="CREAR LOBBY"]', "click_element")
        self.browser.input_text_when_element_is_visible('//input[@id="lobbyname"]', new_lobby)
        self.browser.input_text_when_element_is_visible('//input[@id="lobbypassword"]', new_lobby)
        self.browser.input_text_when_element_is_visible('//input[@id="lobbymoney"]', "100")
        act_on_element('//button[@name="createlobby" and @type="submit"]', "click_element")
        self.lobby = new_lobby

    def register_new_user(self):
            """
            Function thar registers a new user.
            """
            new_user = "RPATRAININGN15"
            self.browser.go_to(self.mundialitis_url)
            self.browser.input_text_when_element_is_visible('//input[@id="rusername"]', new_user)
            self.browser.input_text_when_element_is_visible('//input[@id="rpassword"]', new_user)
            self.browser.input_text_when_element_is_visible('//input[@id="rpassword2"]', new_user)
            act_on_element('//button[@name="register" and @type="submit"]', "click_element")

            self.browser.input_text_when_element_is_visible('//input[@id="rfirstname"]', "RPAN")
            self.browser.input_text_when_element_is_visible('//input[@id="rlastname"]', "RPAN")
            self.browser.input_text_when_element_is_visible('//input[@id="remail"]', "rpantraining@gmail.com")
            self.browser.input_text_when_element_is_visible('//input[@id="raddress"]', "RPAN ADDRESS")
            
            act_on_element('//select[@id="rcountry"]', "click_element")
            act_on_element('//select[@id="rcountry"]/option[@value="Perú"]', "click_element")
            self.browser.input_text_when_element_is_visible('//input[@id="rmoney"]', "100")
            act_on_element('//button[@name="cmpregister" and @type="submit"]', "click_element")
            
            act_on_element('//div[@id="main"]', "find_element")

    def join_lobby(self, mode: str):
        """
        Function that joins an specified lobby.
        """
        act_on_element('//a[@href="/trivialobbies"]', "click_element")
        if mode == "creator":
            act_on_element('//li[@class="list-group-item"]/a[text() = "{}"]'.format("{} - Unido".format(self.lobby)), "click_element")
        else:
            act_on_element('//li[@class="list-group-item"]/a[text() = "{}"]'.format(self.lobby), "click_element")
            self.browser.input_text_when_element_is_visible('//input[@id="lobbypassword"]', self.lobby)
            act_on_element('//button[@id="accesslobby"]', "click_element")
            act_on_element('//button[@id="joinlobby"]', "click_element")

    def start_game(self):
        """
        Function that start the game with the user that created the lobby.
        """
        act_on_element('//button[text() = "INICIAR JUEGO"]', "click_element")
        act_on_element('//button[text() = "Difícil"]', "click_element")

    def play_game(self):
        """
        Function that plays the trivia game.
        """
        questions_remaining = True
        while questions_remaining:
            try:
                act_on_element('//div[@class="list-group"]', "find_element")
            except:
                questions_remaining = False
            else:
                answer_elements = act_on_element('//button[contains(@id, "optn") and position()>1]', "find_elements")
                selected_answer_index = random.randint(0, len(answer_elements) - 1)
                act_on_element(answer_elements[selected_answer_index], "click_element")
                act_on_element('//a[text()="Siguiente" and @class="btn btn-lg mt-4 btn-outline-light"]', "click_element")
        results = act_on_element('//li[@class="list-group-item"]', "find_element").text.split(": ")
        log_message("Username: {}".format(results[0]))
        log_message("Score: {}".format(results[1]))
        capture_page_screenshot(OUTPUT_FOLDER, "Mundialitis_Trivia_Results")




