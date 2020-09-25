from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

import csv
import os.path
import time

# Login
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get('https://www.forexfactory.com/ratmach')

with open('grab2.html', 'w') as f:
    f.write(driver.page_source)

print("Page source written to disk.")
    
time.sleep(60)

# Close browser
driver.quit()
