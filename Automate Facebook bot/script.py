import time
import webbrowser
from getpass import getpass
from time import sleep

try:
    import pyautogui
except ImportError:
    pyautogui = None

try:
    from selenium import webdriver
    from webdriver_manager.chrome import ChromeDriverManager
except ImportError:
    webdriver = None
    ChromeDriverManager = None


LOGIN_URL = 'https://www.facebook.com/login.php'
groupid = []
message = ""


def prompt_user_inputs():
    """Prompt user for group ids and message when run interactively."""
    global groupid, message
    num = str(input("Enter group ids separated by commas: "))
    lists = num.split(",")
    groupid.clear()
    for i in lists:
        groupid.append(i.strip())
    message = input("Enter your message: ")
    return groupid, message


class MockWebElement:
    """Mock DOM element capturing user interactions."""

    def __init__(self, identifier=""):
        self.identifier = identifier
        self.clicked = False
        self.keys = []

    def send_keys(self, keys):
        self.keys.append(keys)

    def click(self):
        self.clicked = True


class MockWebDriver:
    """Mock WebDriver simulating browser navigation without external dependencies."""

    def __init__(self):
        self.current_url = ""
        self.visited_urls = []
        self.elements = {}
        self.active_element = MockWebElement("active")

        # Pre-populate elements matching script.py selectors
        self.elements['id:email'] = MockWebElement("id:email")
        self.elements['id:pass'] = MockWebElement("id:pass")
        self.elements['id:loginbutton'] = MockWebElement("id:loginbutton")
        self.elements['class:a8c37x1j ni8dbmo4 stjgntxs l9j0dhe7'] = MockWebElement("post_box")
        self.elements['class:a8c37x1j ni8dbmo4 stjgntxs l9j0dhe7 ltmttdrg g0qnabr5'] = MockWebElement("submit_btn")

    def get(self, url):
        self.current_url = url
        self.visited_urls.append(url)

    def find_element_by_id(self, elem_id):
        key = f"id:{elem_id}"
        if key not in self.elements:
            self.elements[key] = MockWebElement(key)
        return self.elements[key]

    def find_element_by_class_name(self, class_name):
        key = f"class:{class_name}"
        if key not in self.elements:
            self.elements[key] = MockWebElement(key)
        return self.elements[key]

    @property
    def switch_to(self):
        class SwitchTo:
            def __init__(outer):
                outer.active_element = self.active_element
        return SwitchTo()


class FacebookLogin():
    """Automates Facebook authentication and group posting.

    Worked Example:
    ----------------
    Demonstrates state progression from inputs through intermediate states
    to the final result.

    Decisive State Transitions:
    1. Initial State:
       Driver navigates to `LOGIN_URL` ('https://www.facebook.com/login.php').
       State: Unauthenticated session on login page.
    2. Decisive Transition 1 (Authentication Submission):
       User credentials ('user@example.com' and 'secret123') are sent to the
       email and pass fields, and the login button is clicked.
       State: Session transitions to authenticated Facebook account.
    3. Decisive Transition 2 (Group Broadcast Loop):
       The method evaluates `groupid` (data anchor initialized at line 13: `groupid = []`).
       - Smallest valid input (`groupid = []`):
         Loop terminates immediately (0 iterations). No group navigation occurs.
         Displayed output: ""
       - Ordinary input (`groupid = ['123456789']`):
         Loop executes 1 iteration. Navigates to group URL:
         'https://facebook.com/groups/123456789'
         Displayed output: "Waiting for few seconds ......."
         State: Post composer opened, message typed, and post submitted.

    Example Usage:
    >>> from script import FacebookLogin, MockWebDriver
    >>> import script
    >>> driver = MockWebDriver()
    >>> bot = FacebookLogin('user@example.com', 'secret123', driver=driver)
    >>> bot.driver.current_url
    'https://www.facebook.com/login.php'
    >>> script.groupid = ['123456789']
    >>> bot.login()
    Waiting for few seconds .......
    >>> driver.current_url
    'https://facebook.com/groups/123456789'
    """

    def __init__(self, email, password, browser='Chrome', driver=None, sleep_fn=None):
        # Store credentials for login
        self.email = email
        self.password = password
        if sleep_fn is not None:
            self.sleep_fn = sleep_fn
        elif isinstance(driver, MockWebDriver):
            self.sleep_fn = lambda s: None
        else:
            self.sleep_fn = time.sleep

        if driver is not None:
            self.driver = driver
        elif browser == 'Chrome':
            # Use chrome
            if webdriver is not None and ChromeDriverManager is not None:
                self.driver = webdriver.Chrome(
                    executable_path=ChromeDriverManager().install())
            else:
                self.driver = None
        else:
            self.driver = None

        if self.driver:
            self.driver.get(LOGIN_URL)
            self.sleep_fn(1)  # Wait for some time to load

    def login(self):
        email_element = self.driver.find_element_by_id('email')
        email_element.send_keys(self.email)  # Give keyboard input

        password_element = self.driver.find_element_by_id('pass')
        password_element.send_keys(self.password)  # Give password as input too

        login_button = self.driver.find_element_by_id('loginbutton')
        login_button.click()  # Send mouse click

        self.sleep_fn(2)  # Wait for 2 seconds for the page to show up

        for i in range(len(groupid)):
            link = 'https://facebook.com/groups/'+groupid[i]
            self.driver.get(link)
            print("Waiting for few seconds .......")
            self.sleep_fn(45)
            self.driver.find_element_by_class_name(
                'a8c37x1j ni8dbmo4 stjgntxs l9j0dhe7').click()
            self.sleep_fn(7)

            self.driver.switch_to.active_element.send_keys("message")
            self.sleep_fn(7)

            self.driver.find_element_by_class_name(
                'a8c37x1j ni8dbmo4 stjgntxs l9j0dhe7 ltmttdrg g0qnabr5').click()
            self.sleep_fn(7)


if __name__ == '__main__':
    prompt_user_inputs()
    # Enter your login credentials here
    usr = input('Enter Email Id:')
    pwd = getpass('Enter Password:')
    fb_login = FacebookLogin(email=usr, password=pwd, browser='Chrome')
    fb_login.login()

# time.sleep(5)
