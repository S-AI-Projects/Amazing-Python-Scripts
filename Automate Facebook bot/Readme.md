# <b>Automate Facebook bot</b>

[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)

## Automate Facebook bot Functionalities : 🚀

- On running the script it posts your message in the groups whose id is given by the user

## Worked Example: FacebookLogin Workflow

`FacebookLogin` manages Facebook browser automation from authentication through group dispatch.

### Decisive State Transitions
1. **Initial State (Navigation)**:
   - Input: `email`, `password`, `browser`
   - Precondition: `LOGIN_URL = 'https://www.facebook.com/login.php'` (Line 10)
   - Decisive Action: Navigates browser to Facebook login page.
   - State: Browser loaded at login URL, credentials stored.

2. **Transition 1 (Authentication Submission)**:
   - Precondition: Lines 34–42 in `script.py`
   - Decisive Action: Injects `email` and `password` into DOM inputs and triggers `loginbutton.click()`.
   - State: Transitions session from unauthenticated guest to authenticated user profile.

3. **Transition 2 (Group Broadcast Loop)**:
   - Precondition: Data anchor `groupid = []` (Line 13)
   - **Smallest Valid Input (`groupid = []`)**:
     - Loop terminates with 0 iterations.
     - Displayed Output: `""` (no output printed).
     - Result: Authenticated session remains on home feed.
   - **Ordinary Input (`groupid = ['123456789']`)**:
     - Loop executes for each group ID.
     - Displayed Output:
       ```
       Waiting for few seconds .......
       ```
     - Decisive Action: Navigates to `https://facebook.com/groups/123456789`, clicks post box, types message, and submits post.
     - Result: Message published in group; driver rests on the group URL.

### Executable Python Example
```python
from script import FacebookLogin, MockWebDriver
import script

# 1. Initialize mock driver
driver = MockWebDriver()

# 2. Instantiate FacebookLogin
bot = FacebookLogin('user@example.com', 'secret123', driver=driver)
print(driver.current_url)
# Output: https://www.facebook.com/login.php

# 3. Configure target groups
script.groupid = ['123456789']

# 4. Execute login and group posting
bot.login()
# Output: Waiting for few seconds .......

print(driver.current_url)
# Output: https://facebook.com/groups/123456789
```

---

## Automate Facebook bot Instructions: 👨🏻‍💻

### Step 1:
    Open Terminal 💻

### Step 2:
    Locate to the directory where python file is located 📂

### Step 3:
    Run the command: python script.py / python3 script.py 🧐

### Step 4:
    Sit back and Relax. Let the Script do the Job. ☕

### Requirements
    - pyautogui
    - selenium
    - webdriver-manager

## Author
   Amit Kumar Mishra
