# Getting Started with the bot
<ol>
  <li>Download this github repo as zip</li>
  <li>Note: please install python3 & pip3 if you haven't -> search online tutorial ~_~</li>
</ol>

## What you should edit in python file before running application
### open bot.py file from this folder and edit your personal info including:
<ol>
  <li>concert_id = '45718'</li>
  <li>concert_date = "2023-06-10"</li>
  <li>concert_time = "17:00"</li>
  <li>chromedrive_path = '/Users/krystal/Downloads/chromedriver_mac64/chromedriver'</li>
  <li>payment_option = "pp" (paypal) or "cc" (credit card)</li>
</ol>

## How to run this project
In the project directory, run these in order:

### 1. Open terminal
open terminal on your macbook

### 2. Enter command `cd <dir_to_this_proj_folder_on_your_pc>`
move on to that project folder directory
-> ex. if you download this folder, then usually its `cd Download/concert_ticket_bot`

### 3. Enter command `bot/bin/activate`
activate the bot virtual environment

### 4. Enter command `pip3 install selenium` and `pip3 install python-dotenv`
intall selenium & dotenv module if you haven't. may show error if alr installed but you can ignore

### 5. Download chromedriver
visit https://sites.google.com/a/chromium.org/chromedriver/ & download based on your current chrome version <br>
-> check your chrome version by clicking 3dots on top right of chrome browser & click "Help > About Google Chrome"

### 6. start chromedriver
go to your folder after downloading chromedriver, right click on chromedriver & click "open with terminal"

### 7. Download .env & cookies.pkl file from Google drive link
download the file from provided google drive link

### 8. put these 2 download files into project folder directory
-> ex. you can move this to `concert_ticket_bot` folder (the folder where you download)

### 9. start application - enter command `python3 bot.py`
run this python file will open new chrome browser and enter stuff<br>
<strong>-> this application will still require you to 1) pick seat & 2) confirm payment MANUALLY!!!!</strong><br>
-> if you see some error shown on website, for example entering information, just click next bec bot may click btn too fast