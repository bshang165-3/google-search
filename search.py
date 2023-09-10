from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
from PIL import Image

import concurrent.futures
import io
import time
import random
import os
import pickle
import sys
import csv
from datetime import datetime

def get_timestamp():
    timestamp = datetime.now()
    timestr = str(timestamp).replace(' ', '_')
    timestr = timestr.replace(':', '-')
    timestr = timestr[:-7]
    return timestr

def full_page_screenshot(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    parts = []
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") # Scroll down to bottom
        time.sleep(random.uniform(2.1, 2.9)) # Wait to load page
        part = Image.open(io.BytesIO(driver.get_screenshot_as_png()))
        parts.append(part)
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    # Combine images into one
    full_img = Image.new('RGB', (parts[0].width, sum(p.height for p in parts)))
    offset = 0
    for part in parts:
        full_img.paste(part, (0, offset))
        offset += part.height
    return full_img

def main():
    chromedriver_executable = Service('chromedriver')
    options = Options()
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--headless") 
    options.add_argument("--no-sandbox")
    options.add_argument("--incognito")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled") 
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-extensions")
    options.add_argument('--ignore-ssl-errors')
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features")
    driver = webdriver.Chrome(service = chromedriver_executable, options = options)
    driver.set_window_size(1920, 1080*4)
    #options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")
    user_agent = driver.execute_script("return window.navigator.userAgent")
    is_webdriver = driver.execute_script("return window.navigator.webdriver")
    # Print the user agent
    print("User Agent:", user_agent)
    print("Webdriver is", is_webdriver)
    #driver.maximize_window()
    # wait = WebDriverWait(driver, 20)
    all_urls = []
    all_titles = []

    query_string = folder_string = ""
    for query in sys.argv[1:]:
        if query != "-NV":
            query_string += query + "+"
            folder_string += query + "_"
    query_string = query_string[:-1]
    folder_string = folder_string[:-1]
    
    os.system(f'mkdir screenshots > /dev/null 2>&1')
    os.system(f'mkdir csv > /dev/null 2>&1')
    os.system(f'mkdir screenshots/{folder_string} > /dev/null 2>&1')
    os.system(f'mkdir csv/{folder_string} > /dev/null 2>&1')

    try:
        orig_url = "https://www.google.com/search?q=" + query_string
        
        driver.get(orig_url)
        time.sleep(random.uniform(2.3, 2.9))
        #image = full_page_screenshot(driver)
        #image.save(f"screenshots/{folder_string}/0_{get_timestamp()}.png")
        driver.save_screenshot(f"screenshots/{folder_string}/0_{get_timestamp()}.png")
        all_urls.append(orig_url)
        all_titles.append(query_string)
    except Exception as e:
        print(f"Failed to get original URL {orig_url}")
        return

    for i in range(1, 20):
        if i > 10:
            break
        time.sleep(random.uniform(2.1, 3.1))
        for j in range(3, 10):
            try:
                search_result_xpath = f"//div[{i}]" + "/div" * j + "/a/h3"
                link = driver.find_element(By.XPATH, f"{search_result_xpath}")
                x = int(driver.find_element(By.XPATH, f"{search_result_xpath}").location['x'])
                y = int(driver.find_element(By.XPATH, f"{search_result_xpath}").location['y'])
                width = int(driver.find_element(By.XPATH, f"{search_result_xpath}").size['width'])
                height = int(driver.find_element(By.XPATH, f"{search_result_xpath}").size['height'])
                print(search_result_xpath)
                text = link.text
                if text == "" or text == "More results":
                    continue
                print("Text is:", text)
                action = webdriver.common.action_chains.ActionChains(driver)
                action.move_by_offset(x + width/2, y + height/2)
                action.click()
                action.perform()
                time.sleep(random.uniform(2.1, 3.1))
                action.reset_actions()
                action.perform()
                break
            except Exception as e:
                pass

        time.sleep(random.uniform(1.1, 1.9))
        curr_url = driver.current_url
        if "google.com" in curr_url:
            print("google in url; wrong url")
            driver.get(orig_url)
            continue
        print("Getting URL:", curr_url)
        try:
            image = full_page_screenshot(driver)
            image.save(f"screenshots/{folder_string}/{i}_{get_timestamp()}.png")
            #driver.save_screenshot(f"screenshots/{folder_string}/{i}_{get_timestamp()}.png")
            print(f"Screenshot saved for {curr_url}")
            all_urls.append(curr_url)
            all_titles.append(text)
        except Exception as e:
            print(e)
            print(f"Failed to save screenshot for {curr_url}")
        driver.get(orig_url)
        time.sleep(random.uniform(0.2, 0.5))
    
    for title in all_titles:
        title = title.replace(",", "_")
    
    with open(f"csv/{folder_string}/{get_timestamp()}.csv", "w") as f:
        writer = csv.writer(f)
        if len(all_urls) == len(all_titles):
            for idx, url in enumerate(all_urls):
                writer.writerow([idx, url, all_titles[idx]])
        else:
            for idx, url in enumerate(all_urls):
                writer.writerow([idx, url])

    print("Done! Quitting!")

if __name__ == "__main__":
    main()