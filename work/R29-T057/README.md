# Task R29-T057: Publish a runnable example for FacebookLogin (script.py)

## Overview
- **Item**: Automate Facebook bot
- **Target File**: `Automate Facebook bot/script.py`
- **Target Class**: `FacebookLogin`
- **Task Type**: Executable documentation
- **Source Anchor**: `groupid = []` (Line 13)

---

## 1. Documentation & Worked Example

The documentation for `FacebookLogin` has been added to its docstring in `script.py` and to `Automate Facebook bot/Readme.md`.

### Decisive State Transitions
1. **Initial State (Navigation)**:
   - Inputs: `email`, `password`, `browser='Chrome'` (with optional `driver` for test injection).
   - Precondition: `LOGIN_URL = 'https://www.facebook.com/login.php'` (Line 10).
   - The driver navigates to `LOGIN_URL`.
   - State: Guest session on Facebook login portal.

2. **Decisive Transition 1 (Authentication Submission)**:
   - Preconditions: Lines 34–42 in `script.py`.
   - Credentials are submitted:
     - `email_element.send_keys(self.email)`
     - `password_element.send_keys(self.password)`
     - `login_button.click()`
   - State: Session transitions from unauthenticated guest to authenticated account session.

3. **Decisive Transition 2 (Group Broadcast Loop)**:
   - Preconditions: Data anchor `groupid = []` (Line 13), loop at lines 45–60.
   - **Smallest Valid Input (`groupid = []`)**:
     - Loop terminates after 0 iterations (`len(groupid) == 0`).
     - Displayed Output: `""` (no output printed).
     - Final URL: Remains on `LOGIN_URL` (or feed).
   - **Ordinary Input (`groupid = ['123456789']`)**:
     - Loop executes 1 iteration.
     - Navigates to `https://facebook.com/groups/123456789`.
     - Displayed Output:
       ```
       Waiting for few seconds .......
       ```
     - Clicks post compose element, enters message, and clicks submit.
     - Final URL: `https://facebook.com/groups/123456789`.

---

## 2. Preconditions and Fixtures

### Preconditions Table
| Precondition | Source Line | Description |
|---|---|---|
| `LOGIN_URL` | Line 10 | Target login URL `https://www.facebook.com/login.php` |
| `groupid = []` | Line 13 | Source fixture/data anchor for target groups |
| `__init__` | Lines 22–31 | Credentials storage and initial navigation |
| `login` submit | Lines 34–44 | Credential entry and login button click |
| Group broadcast loop | Lines 45–60 | Group navigation, waiting prompt, and message submission |

### Fixtures
1. **Smallest Valid Input**:
   - `email = 'test_user@example.com'`, `password = 'password123'`, `groupid = []`
   - Expected Output: `""`
   - Expected Final URL: `'https://www.facebook.com/login.php'`
2. **Ordinary Input**:
   - `email = 'ordinary_user@example.com'`, `password = 'secure_password_456'`, `groupid = ['123456789']`
   - Expected Output: `"Waiting for few seconds .......\n"`
   - Expected Final URL: `'https://facebook.com/groups/123456789'`

---

## 3. Automated Verification

Run checks locally:
```bash
python3 work/R29-T057/check.py
```
Or via unittest:
```bash
python3 -m unittest discover -s "Automate Facebook bot/tests" -p "test_script.py" -v
```
Evidence is stored in `work/R29-T057/results.json` and `work/R29-T057/results.txt`.
