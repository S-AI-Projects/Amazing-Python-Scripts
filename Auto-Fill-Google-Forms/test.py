import csv
import time

try:
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
except ImportError:
    webdriver = None
    Keys = None

inputName = '/html/body/div/div[2]/form/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input'
inputEmailID = '/html/body/div/div[2]/form/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input'
inputPhone = '/html/body/div/div[2]/form/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input'

# Submit Button Xpath
Submit = '/html/body/div/div[2]/form/div[2]/div/div[3]/div[1]/div/div'


def sleep():
    time.sleep(3)


def read_records(f_input):
    """
    Parse form records from an opened CSV file or stream.

    Precondition anchors:
    - Line 27: csv_input = csv.DictReader(f_input)
    - Lines 28-31: row['name'], row['email'], row['phone_number']
    """
    name = []
    email = []
    phone = []
    csv_input = csv.DictReader(f_input)
    for row in csv_input:
        name.append(row['name'])
        email.append(row['email'])
        phone.append(row['phone_number'])
    return name, email, phone


def fill_form_records(name, email, phone, browser=None, sleep_fn=None):
    """
    Execute form fill-out and submission loop for extracted record lists.

    Precondition anchors:
    - Lines 6-8: input XPaths
    - Line 11: Submit button XPath
    - Lines 36-45: Submission loop over records
    """
    if sleep_fn is None:
        sleep_fn = sleep

    submissions = []
    i = 0
    while i < len(name):
        record = {
            'name': name[i],
            'email': email[i],
            'phone_number': phone[i]
        }
        if browser is not None:
            browser.find_element_by_xpath(inputName).send_keys(name[i])
            browser.find_element_by_xpath(inputEmailID).send_keys(email[i])
            browser.find_element_by_xpath(inputPhone).send_keys(phone[i])
            sleep_fn()
            browser.find_element_by_xpath(Submit).click()
            sleep_fn()
            browser.back()
            sleep_fn()
        submissions.append(record)
        i += 1
    return submissions


def main():
    browswer = webdriver.Firefox(
        executable_path=r'C:\geckodriver-v0.28.0-win64\geckodriver.exe')
    browswer.get(
        'https://docs.google.com/forms/d/e/1FAIpQLScBejWF809oacjZlvkciXREi50fyHcq75l988KDJo3ycG7xkg/viewform'
    )
    with open("input.csv", "r") as f_input:
        name, email, phone = read_records(f_input)

    fill_form_records(name, email, phone, browser=browswer)
    browswer.quit()


if __name__ == '__main__':
    main()
