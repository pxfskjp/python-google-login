from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import pyautogui
from time import sleep
import csv

Time = 5
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.set_window_size(600, 850)
current_gmail = ""

def get_company_list () :
    global current_gmail
    print("Get data from company_lists.csv...")
    with open('company_lists.csv', newline='') as csvfile:
        company_lists = csv.DictReader(csvfile)
        for num, row in enumerate(company_lists, start=0) :
            row = row['gmail;password;company_name;rates;review;recoverymail'].split(';')
            Gmail, Pass, RecoveryMail = row[0], row[1], row[5]
            company_name, company_rates, company_review = row[2], row[3], row[4]
            print(f"Gmail : {Gmail}, Pass : {Pass}, RecoveryMail : {RecoveryMail}, Company Name : {company_name}, Company Reates {company_rates}, Company Review {company_review}, \n")
            if num == 0 :
                google_sign_in(Gmail, Pass, RecoveryMail)
                sleep(Time)
                find_company_and_give_review(Gmail, company_name, company_rates, company_review)

            elif current_gmail != Gmail :
                print("Log in again")
                signout_btn = driver.find_element_by_id('gb').find_element_by_xpath('//div/div/div/div[2]/div/a')
                driver.execute_script("arguments[0].click();", signout_btn)
                sleep(Time)
                sign_out = driver.find_element_by_id('gb_71')
                driver.execute_script("arguments[0].click();", sign_out)
                sleep(Time)
                google_sign_in(Gmail, Pass, RecoveryMail)
                sleep(Time)
                find_company_and_give_review(Gmail, company_name, company_rates, company_review)

            else :
                find_company_and_give_review(Gmail, company_name, company_rates, company_review)

def google_sign_in(email, password, RecoveryMail):
    global current_gmail
    print("Log in Google...")

    sleep(Time)
    pyautogui.typewrite("rb_vps23_team2")
    pyautogui.press('tab')
    pyautogui.typewrite("gbrrtghwerj")
    pyautogui.press('enter')

    driver.get('https://stackoverflow.com/users/signup?ssrc=head&returnurl=%2fusers%2fstory%2fcurrent')
    sleep(10)
    driver.find_element_by_xpath('//*[@id="openid-buttons"]/button[1]').click()
    sleep(Time)
    try :
        driver.find_element_by_class_name('BHzsHc').click()
        sleep(Time)
        driver.find_element_by_xpath('//*[@id="identifierId"]').send_keys(email)
        sleep(Time)
        driver.find_element_by_xpath('//*[@id="identifierId"]').send_keys(Keys.ENTER)
        sleep(Time)
        driver.find_element_by_xpath('//*[@id="password"]/div[1]/div/div[1]/input').send_keys(password)
        driver.find_element_by_xpath('//*[@id="password"]/div[1]/div/div[1]/input').send_keys(Keys.ENTER)
        driver.implicitly_wait(1)
        sleep(Time)

        try :
            recovery_btn = driver.find_element_by_xpath('//ul[contains(@class, "OVnw0d")]/li[1]')
            recovery_btn.click()
            sleep(Time)
        except:
            pass

        try:
            driver.find_element_by_id('knowledge-preregistered-email-response').send_keys(RecoveryMail)
            driver.find_element_by_id('knowledge-preregistered-email-response').send_keys(Keys.ENTER)
        except:
            pass

        current_gmail = email
        print(f"Google Login Success! You loggod in by {email}")

    except NoSuchElementException:
        driver.find_element_by_xpath('//*[@id="identifierId"]').send_keys(email)
        next_btn = driver.find_element_by_xpath('//*[@id="identifierNext"]')
        driver.implicitly_wait(Time)
        next_btn.click()
        driver.implicitly_wait(Time)
        sleep(Time)

        driver.find_element_by_xpath('//*[@id="password"]/div[1]/div/div[1]/input').send_keys(password)
        next_btn = driver.find_element_by_xpath('//*[@id="passwordNext"]')
        driver.implicitly_wait(Time)
        next_btn.click()
        driver.implicitly_wait(1)
        sleep(Time)
        try :
            recovery_btn = driver.find_element_by_xpath('//ul[contains(@class, "OVnw0d")]/li[1]')
            recovery_btn.click()
            sleep(Time)
        except:
            pass
        try:
            driver.find_element_by_id('knowledge-preregistered-email-response').send_keys(RecoveryMail)
            driver.find_element_by_id('knowledge-preregistered-email-response').send_keys(Keys.ENTER)
        except:
            pass
        current_gmail = email
        print(f"Google Login Success! You loggod in by {email}")

def find_company_and_give_review (gmail, name, rates, review) :
    global current_gmail
    print("Find the company for that Gmail on Google Map......")
    print("rates", rates, "gmail", gmail, "name", name)
    driver.get('https://www.google.com/maps/')
    sleep(Time)
    driver.refresh()
    sleep(Time)
    driver.find_element_by_id('searchboxinput').send_keys(name)
    sleep(Time)
    driver.find_element_by_id('searchbox-searchbutton').click()
    sleep(Time)
    img_tag = driver.find_element_by_xpath('//img[contains(@src,"//www.gstatic.com/images/icons/material/system_gm/1x/rate_review_gm_blue_18dp.png")]')
    review_button = img_tag.find_element_by_xpath('..')
    button_name = review_button.find_element_by_tag_name('span').get_attribute('innerHTML')
    if button_name == "Write a review" or button_name == "Escribir una reseña" :
        print("Giving review to the company...")
        review_button.click()
        sleep(Time)
        driver.switch_to.frame(driver.find_element_by_class_name("goog-reviews-write-widget"))
        sleep(Time)
        driver.find_element_by_class_name('Rgwf9b').click()
        sleep(Time)
        driver.find_element_by_xpath(f'//span[contains(@data-rating,{rates})]').click()
        sleep(Time)
        driver.find_element_by_xpath('//textarea[contains(@class,"review-text")]').send_keys(review)
        sleep(Time)
        post_button = driver.find_element_by_xpath('//c-wiz[contains(@class, "SSPGKf")]/div/div/div/div/div[2]/div/div[2]/div/button')
        driver.execute_script("arguments[0].click();", post_button)
        sleep(Time)
        complete_button = driver.find_element_by_xpath('//c-wiz[contains(@class, "SSPGKf")]/div/div/div/div/div/div[2]/div/div/div/button')
        driver.execute_script("arguments[0].click();", complete_button)
        sleep(Time)
    else :
        print("You already give review to this company!")
    
get_company_list()