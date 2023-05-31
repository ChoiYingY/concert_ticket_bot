# Getting Started with the bot
<ol>
  <li>Download this github repo as zip</li>
  <li>Note: please install python3 & pip3 if you haven't -> search online tutorial ~_~</li>
</ol>

## What you should edit in python file before running application
### open bot.py file from this folder and edit your personal info including:
<ol>
  <li>email = "your_yes24_email@gmail.com"</li>
  <li>password = "your_yes24_password"</li>
  <li>concert_id = '45227'</li>
  <li>concert_date = "2023-05-31"</li>
  <li>concert_time = "20:00"</li>
  <li>paypal_email = "your_paypal_email@gmail.com"</li>
  <li>paypal_password = "your_paypal_password"</li>
  <li>chromedrive_path = '/Users/krystal/Downloads/chromedriver_mac64/chromedriver'</li>
</ol>

## How to run this project
In the project directory, run these in order:

### 1. Open terminal
open terminal on your macbook

### 2. Enter command `cd <dir_to_this_proj_folder_on_your_pc>`
move on to that project folder directory
-> ex. if you download this folder, then usually its `cd Download/yes24_ticket_bot`

### 3. Enter command `bot/bin/activate`
activate the bot virtual environment

### 4. Enter command `pip3 install install selenium`
intall selenium module if you haven't. may show error if alr installed but you can ignore

### 5. Download chromedriver
visit https://sites.google.com/a/chromium.org/chromedriver/ & download based on your current chrome version <br>
-> check your chrome version by clicking 3dots on top right of chrome browser & click "Help > About Google Chrome"

### 6. start chromedriver
go to your folder after downloading chromedriver, right click on chromedriver & click "open with terminal"

### 7. open another terminal
once you see "ChromeDriver was started successfully.", open another terminal by clicking '+' button

### 8. start application - enter command `python3 bot.py`
run this python file will open new chrome browser and enter stuff<br>
-> this application still you to pick seat & set up payment method manually<br>
-> if you see some error shown on website, for example entering information, just click next bec bot may click btn too fast