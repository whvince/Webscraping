from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import re
import time

driver = webdriver.Chrome()

driver.get("https://www.yelp.com/biz/obao-new-york-4")

csv_file = open('yelp_reviews_obao.csv', 'w', encoding='utf-8', newline='')
writer = csv.writer(csv_file)

index = 1
while True:
    try:
        print("Scraping Page number " + str(index))
        # Must have a sleep timer for the page to load before moving on to scrape the data. Otherwise, code stops. 
        time.sleep(2)
        index = index + 1
        # Find all the reviews on the page
        wait_review = WebDriverWait(driver, 1)
        # Note Yelp periodically updates its HTML syntax so the following tags may need to be updated
        reviews = wait_review.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="lemon--div__373c0__1mboc spinner-container__373c0__N6Hff border-color--default__373c0__YEvMS"]')))
        
        for review in reviews:
            # Initialize an empty dictionary for each review
            review_dict = {}
           
            text = review.find_element_by_xpath('.//p[@class="lemon--p__373c0__3Qnnj text__373c0__2pB8f comment__373c0__3EKjH text-color--normal__373c0__K_MKN text-align--left__373c0__2pnx_"]').text
            username = review.find_element_by_xpath('.//span[@class="lemon--span__373c0__3997G text__373c0__2pB8f fs-block text-color--inherit__373c0__w_15m text-align--left__373c0__2pnx_ text-weight--bold__373c0__3HYJa"]').text
            location = review.find_element_by_xpath('.//span[@class="lemon--span__373c0__3997G text__373c0__2pB8f text-color--normal__373c0__K_MKN text-align--left__373c0__2pnx_ text-weight--bold__373c0__3HYJa text-size--small__373c0__3SGMi"]').text
            date_published = review.find_element_by_xpath('.//span[@class="lemon--span__373c0__3997G text__373c0__2pB8f text-color--mid__373c0__3G312 text-align--left__373c0__2pnx_"]').text
            rating = review.find_element_by_xpath('.//span[@class="lemon--span__373c0__3997G display--inline__373c0__2q4au border-color--default__373c0__YEvMS"]//div').get_attribute('aria-label')
            rating = float(re.findall('\d+', rating)[0])

            review_dict['text'] = text
            review_dict['username'] = username
            review_dict['location'] = location
            review_dict['date_published'] = date_published 
            review_dict['rating'] = rating

            writer.writerow(review_dict.values())

        # Locate and click the next button on the page.

        wait_button = WebDriverWait(driver, 30)
        next_button = wait_button.until(EC.element_to_be_clickable((By.XPATH, '//div[@class="lemon--div__373c0__1mboc navigation-button-text__373c0__38ysY u-space-l2 border-color--default__373c0__2oFDT"]')))
        next_button.click()

    except Exception as issue:
        print(issue)
        csv_file.close()
        driver.close()
        break