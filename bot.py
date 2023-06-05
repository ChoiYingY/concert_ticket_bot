import os
import time
import pickle
from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

done = False
doneLogin = False
doneSwitchWindow = False
doneClickBook = False
doneSelectDate = False
doneSelectSeat = False
doneDiscount = False
doneDelivery = False
donePayment = False
donePaymentWindow = False

load_dotenv()

# set up login info, preloaded from .env file
email = os.getenv('EMAIL')
password = os.getenv('PASSWORD')
paypal_email = os.getenv('PAYPAL_EMAIL')
paypal_password = os.getenv('PAYPAL_PASSWORD')

# ************** IMPORTANT!!!! Substitute information here **************
# fill in concert info
concert_id = '45718'
concert_date = "2023-06-10"
concert_time = "17:00"
# ^ other testing link, 45711 is shinee concert
# concert_id = '45711'
# concert_date = "2023-06-23"
# concert_time = "19:00"

# fill in path to chromedriver
# chromedrive_path = 'path_to_chromedriver'
chromedrive_path = '/Users/krystal/Downloads/chromedriver_mac64/chromedriver'   # <- my path but plz edit to yours

# choose payment method: paypal(pp) <- curr default payment / credit card (cc) ****
payment_option = "pp"
# payment_option = "cc"
# ^^^^ ************** end of edit **************

# links & paths based on input info ^
concert_time_xpath = f'//li[@timeinfo="{concert_time}"]'
bookLink = f'http://ticket.yes24.com/Pages/English/Perf/FnPerfDeail.aspx?IdPerf={concert_id}'
reservLink = f'http://ticket.yes24.com/Pages/English/Sale/FnPerfSaleProcess.aspx?IdPerf={concert_id}'

# set up cookies & option
# selenium_cookie_file = "cookies.pkl"

# Connect to chrome using driver & open browser
service = Service(chromedrive_path)
service.start()

driver = webdriver.Remote(service.service_url)

# login process
def login():
    global doneLogin

    driver.get('https://ticket.yes24.com/Pages/English/Member/FnLoginNew.aspx?ReturnURL={}'.format(bookLink))
    username_input = driver.find_element(By.ID, "txtEmail")
    password_input = driver.find_element(By.ID, "txtPassword")

    # Enter the login credentials
    username_input.send_keys(email)
    password_input.send_keys(password)

    # Submit the login form
    password_input.send_keys(Keys.ENTER)
    doneLogin = True
    
# main process
def main():
    global done, doneLogin, doneSwitchWindow, doneClickBook, doneSelectDate, doneSelectSeat, doneDiscount, doneDelivery, donePayment, donePaymentWindow, email, password, paypal_email, paypal_password, concert_date, concert_time, payment_option, concert_time_xpath, verifyLink, bookLink, reservLink

    while not done:
        time.sleep(5) # Let the user actually see something!
        
        # step click book btn
        try:
            if driver.current_url == bookLink and not doneClickBook and doneLogin:
                doneLogin = True
                print('step click booking')
                bookBtn = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "span.btntxt")))
                if bookBtn:
                    bookBtn.click()
                    doneClickBook = True
        except Exception as e:
            print("Error on step click booking")
            print(e)
            print('now refresh')
            driver.refresh()

        # step switch to popup window
        try:
            if doneClickBook and not doneSwitchWindow:
                print('step switch window')
                main_window_handle = driver.current_window_handle
                print(main_window_handle)

                for handle in driver.window_handles:
                    driver.switch_to.window(handle)
                    if driver.current_url == reservLink:
                        doneSwitchWindow = True
                        break  # Switched to the desired window, exit the loop
        
        except Exception as e:
            print("Error on step switch window")
            print(e)

        # step select concert date & time
        try:
            if driver.current_url == reservLink and doneSwitchWindow and not doneSelectDate:
                print('step select concert date & time')

                concertDate = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, concert_date)))
                if concertDate:
                    concertDate.click()
                    concertTime = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, concert_time_xpath)))
                    if concertTime:
                        concertTime.click()
                        select_seat_btn = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'btnSeatSelect')))

                        # Now click on select seat btn & start choosing seat
                        if select_seat_btn:
                            select_seat_btn.click()
                            doneSelectDate = True
        except Exception as e:
            print("Error on step select concert date & time")
            print(e)

        # step select concert seat
        try:
            if doneSelectDate and not doneSelectSeat:
                print('step select seat')
                step3 = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "li.m03")))

                while not step3:
                    print('waiting...')
                    step3 = driver.find_element(By.CSS_SELECTOR, "li.m03")

                is_step3 = "m03 on" in step3.get_attribute("class")

                while step3 and not is_step3:
                    print('waiting...')
                    is_step3 = "m03 on" in step3.get_attribute("class")
                    step3 = driver.find_element(By.CSS_SELECTOR, "li.m03")
                
                if is_step3:
                    doneSelectSeat = True
        except Exception as e:
            print("Error on step select seat")
            print(e)

        # step skip discount
        try:
            if doneSelectSeat and not doneDiscount:
                print('step skip discount')
                next_btn = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//a[@class="dcursor" and @onclick="fdc_PromotionEnd();"]')))
                if next_btn:
                    next_btn.click()
                    doneDiscount = True
        except Exception as e:
            print("Error on step skip discount")
            print(e)

        # step set up ticket delivery
        try:
            if doneDiscount and not doneDelivery:
                    print('step select ticket delivery')
                    option = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'rdoDeliveryBase')))

                    if option and option.is_selected():
                        next_btn = driver.find_element(By.XPATH, '//a[@class="dcursor" and @onclick="fdc_DeliveryEnd();"]')
                        if next_btn:
                            next_btn.click()
                            doneDelivery = True
        except Exception as e:
            print("Error on step select ticket delivery")
            print(e)

        # step set up payment method
        try:
            if doneDelivery and not donePayment:
                print('step select payment method')

                check1 = check2 = check3 = False
                third_party_option = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'cbxUserInfoAgree')))
                cancel_fee_option = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'cbxCancelFeeAgree')))
                
                paypal_option = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'rdoPays36711')))
                creditCard_option = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'rdoPays2')))
                
                if third_party_option and not third_party_option.is_selected():
                    third_party_option.click()
                    check1 = True

                if cancel_fee_option and not cancel_fee_option.is_selected():
                    cancel_fee_option.click()
                    check2 = True

                if payment_option == 'pp':
                    if paypal_option:
                        paypal_option.click()
                        check3 = True
                else:
                    if creditCard_option:
                        creditCard_option.click()
                        check3 = True

                if check1 and check2 and check3:
                    pay_btn = driver.find_element(By.XPATH, '//a[@class="dcursor" and @onclick="fdc_PrePayCheck();"]')
                    if pay_btn:
                        pay_btn.click()
                        donePayment = True
        except Exception as e:
            print("Error on step select payment method")
            print(e)

        # try:
        #     if donePayment:
        #         print("step skip modal yes btn")
        #         yes_btn = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, '//button[span[text()="Yes"]]')))
        #         if yes_btn:
        #             print('click yes btn')
        #             yes_btn.click()

        # except Exception as e:
        #     print("Error on step skip modal btn")
        #     print(e)

        # step skip modal btn
        try:
            if donePayment:
                print("step skip modal yes btn")
                if donePayment:
                    if payment_option == 'pp':
                        print("paypal")
                        ok_btn = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, '//button[span[text()="OK"]]')))
                        if ok_btn:
                            print('click ok btn')
                            ok_btn.click()
                            donePaymentWindow = True
                    else:
                        donePaymentWindow = True
        except Exception as e:
            print("Error on step skip modal btn")
            print(e)

        # step pay
        try:
            if donePayment:
                print("step pay")
                if donePaymentWindow:
                    if payment_option == 'pp':
                        main_window_handle = driver.current_window_handle

                        for handle in driver.window_handles:
                            driver.switch_to.window(handle)
                            if 'www.paypal.com' in driver.current_url:
                                break  # Switched to the desired window, exit the loop

                        if 'www.paypal.com' in driver.current_url:
                            print(driver.current_url)
                            email_input = driver.find_element(By.ID, "email")
                            if email_input:
                                email_input.send_keys(paypal_email)
                                email_input.send_keys(Keys.ENTER)

                            password_input = WebDriverWait(driver, 100).until(EC.visibility_of_element_located((By.ID, "password")))
                            if password_input:
                                password_input.send_keys(paypal_password)
                                password_input.send_keys(Keys.ENTER)
                    else:
                        print('credit card')
                        close_discount = WebDriverWait(driver, 100).until(EC.visibility_of_element_located((By.ID, 'closeCpnBtn')))
                        if close_discount:
                            close_discount.click()
        except Exception as e:
            print("Error on step paypal")
            print(e)

            if done: 
                driver.quit()

if __name__ == '__main__':
    try:
        with open("cookies.pkl", "rb") as file:
            cookies = pickle.load(file)
            
        # navigate to login page, and redirect back to ticket page once login
        driver.get(bookLink)
        
        for cookie in cookies:
            driver.add_cookie(cookie)

        driver.refresh()
        doneLogin = True
    
    except Exception as e:
        print("Error")
        print(e)

        print('step login')
        login()
       
    main()