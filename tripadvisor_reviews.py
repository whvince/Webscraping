from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import re
import time

driver = webdriver.Chrome()

driver.get("https://www.tripadvisor.com/Restaurant_Review-g60763-d3263717-Reviews-Obao-New_York_City_New_York.html")
            
# Click all language button
all_lang_button = driver.find_element_by_xpath('//span[@class="checkmark"]')
all_lang_button.click()


csv_file = open('tripadvisor_reviews_obao.csv', 'w', encoding='utf-8', newline='')
writer = csv.writer(csv_file)

index = 1

while True:
    try:
        print("Scraping Page number " + str(index))
        # Must have a sleep timer for the page to load before moving on to scrape the data. Otherwise, code stops. 
        time.sleep(2)
        index = index + 1
        
        # Find all the reviews on the page
        wait_review = WebDriverWait(driver, 10)
        reviews = wait_review.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="prw_rup prw_reviews_review_resp"]')))
        
        for review in reviews:
            # Initialize an empty dictionary for each review
            review_dict = {}
             
             # Get location of the user. If not, fill in blank.  

            try:
                location = review.find_element_by_xpath('.//div[@class="userLoc"]').text
            except:
                location = ""

            title = review.find_element_by_xpath('.//span[@class="noQuotes"]').text
            text = review.find_element_by_xpath('.//div[@class="prw_rup prw_reviews_text_summary_hsx"]').text
            username = review.find_element_by_xpath('.//div[@class="info_text pointer_cursor"]//div').text
            contribution = review.find_element_by_xpath('.//span[@class="badgetext"]').text
            date_published = review.find_element_by_xpath('.//div[@class="prw_rup prw_reviews_stay_date_hsx"]').text
            data_published_backup = review.find_element_by_xpath('.//span[@class="ratingDate"]').get_attribute('title')
            rating = review.find_element_by_xpath('.//div[@class="ui_column is-9"]//span').get_attribute('class')
            rating = int(re.findall('\d+', rating)[0])/10

            review_dict['title'] = title
            review_dict['text'] = text
            review_dict['username'] = username
            review_dict['location'] = location
            review_dict['contribution'] = contribution
            review_dict['date_published'] = date_published
            review_dict['data_published_backup'] = data_published_backup
            review_dict['rating'] = rating

            writer.writerow(review_dict.values())
        
        # Locate and click the next button on the page.
        
        wait_button = WebDriverWait(driver, 100)
        next_button = wait_button.until(EC.element_to_be_clickable((By.XPATH, '//a[@class="nav next ui_button primary"]')))
        next_button.click()

    except Exception as e:
        print(e)
        csv_file.close()
        driver.close()
        break