import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

done = False
doneLogin = False
doneClickBook = False
doneSelectDate = False
doneSelectSeat = False
doneDiscount = False
doneDelivery = False
donePayment = False
donePaymentWindow = False

# **** IMPORTANT!!!! Substitute information here ****
email = "your_yes24_email@gmail.com"
password = "your_yes24_password"
concert_id = '45227'
concert_date = "2023-05-31"
concert_time = "20:00"
paypal_email = "your_paypal_email@gmail.com"
paypal_password = "your_paypal_password"
chromedrive_path = '/Users/krystal/Downloads/chromedriver_mac64/chromedriver'

# **** IMPORTANT!!!! Choose pay with paypal(pp) <- curr default payment / credit card (cc) ****
payment_option = "pp"
# payment_option = "cc"

# links & paths based on input info ^
concert_time_xpath = f'//li[@timeinfo="{concert_time}"]'
bookLink = f'http://ticket.yes24.com/Pages/English/Perf/FnPerfDeail.aspx?IdPerf={concert_id}'
reservLink = f'http://ticket.yes24.com/Pages/English/Sale/FnPerfSaleProcess.aspx?IdPerf={concert_id}'

# Connect to chrome using driver & open browser
service = Service(chromedrive_path)

service.start()

driver = webdriver.Remote(service.service_url)

# navigate to login page, and redirect back to ticket page once login
driver.get('https://ticket.yes24.com/Pages/English/Member/FnLoginNew.aspx?ReturnURL={}'.format(bookLink))

while not done:
    time.sleep(5) # Let the user actually see something!

    try:
        if not doneLogin:
            username_input = driver.find_element(By.ID, "txtEmail")
            password_input = driver.find_element(By.ID, "txtPassword")

            # Enter the login credentials
            username_input.send_keys(email)
            password_input.send_keys(password)

            # Submit the login form
            password_input.send_keys(Keys.ENTER)
            doneLogin = True

        if driver.current_url == bookLink and not doneClickBook:
            doneLogin = True
            bookBtn = driver.find_element(By.CSS_SELECTOR, "span.btntxt")
            if bookBtn:
                bookBtn.click()
                doneClickBook = True

            main_window_handle = driver.current_window_handle
            popup_window_handle = None

            for handle in driver.window_handles:
                if handle != main_window_handle:
                    popup_window_handle = handle
                    break

            driver.switch_to.window(popup_window_handle)

            if driver.current_url == reservLink and doneClickBook and not doneSelectDate:
                concertDate = driver.find_element(By.ID, concert_date)
                if concertDate:
                    concertDate.click()
                    concertTime = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, concert_time_xpath)))
                    if concertTime:
                        concertTime.click()
                        select_seat_btn = driver.find_element(By.ID, 'btnSeatSelect')

                        # Now click on select seat btn & start choosing seat
                        if select_seat_btn:
                            select_seat_btn.click()
                            doneSelectDate = True
            
            if doneSelectDate and not doneSelectSeat:
                step3 = driver.find_element(By.CSS_SELECTOR, "li.m03")

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

            if doneSelectSeat and not doneDiscount:
                print('step3')
                next_btn = driver.find_element(By.XPATH, '//a[@class="dcursor" and @onclick="fdc_PromotionEnd();"]')
                if next_btn:
                    next_btn.click()
                    doneDiscount = True

            if doneDiscount and not doneDelivery:
                print('step4')
                option = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'rdoDeliveryBase')))

                if option and option.is_selected():
                    next_btn = driver.find_element(By.XPATH, '//a[@class="dcursor" and @onclick="fdc_DeliveryEnd();"]')
                    if next_btn:
                        next_btn.click()
                        doneDelivery = True

            if doneDelivery and not donePayment:
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

            if donePayment:
                yes_btn = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, '//button[span[text()="Yes"]]')))
                if yes_btn:
                    yes_btn.click()

                    if payment_option == 'pp':
                        ok_btn = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, '//button[span[text()="OK"]]')))
                        if ok_btn:
                            ok_btn.click()
                            donePaymentWindow = True
                    else:
                        donePaymentWindow = True

            if donePaymentWindow:
                if payment_option == 'pp':
                    main_window_handle = driver.current_window_handle
                    popup_window_handle = None

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
        print("Error")
        print(e)

driver.quit()