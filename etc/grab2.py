from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

import csv
import os.path


# Login
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get('https://www.forexfactory.com/ratmach')

with open('page.html', 'w') as f:
    f.write(driver.page_source)

# Close browser
driver.quit()
