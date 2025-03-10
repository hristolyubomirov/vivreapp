from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import time
import csv
import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('vivre_data.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)

# enable the browser you have installed or want to use. Currently it's set to Chrome.
    #driver = webdriver.Firefox()
    #driver = webdriver.Edge()
    #driver = webdriver.Safari()
    driver = webdriver.Chrome()

    url = 'https://www.vivre.bg/s-1056/kanapeta-i-aglovi-kanapeta'
    driver.get(url)

    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'item-product')))

    products = driver.find_elements(By.CLASS_NAME, 'item-product')
    product_links = [product.find_element(By.TAG_NAME, 'a').get_attribute('href') for product in products]

    for product_index, product_url in enumerate(product_links):
        if len(driver.window_handles) > 1:
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                time.sleep(1)
        try:
            driver.execute_script("window.open(arguments[0], '_blank');", product_url)
            driver.switch_to.window(driver.window_handles[1])
            time.sleep(1) 

            title = driver.find_element(By.TAG_NAME, 'h1').text
            print(f"Processing product: {title}")

            try:
                exp_pr = driver.find_element(By.CSS_SELECTOR, 'span.price-rrp').text + ' Промоция = Да'
            except NoSuchElementException:
                exp_pr = "This item has no recommended price. Промоция = Не"

            try:
                fast_del = driver.find_element(By.CSS_SELECTOR, 'span.label.label-success').text
            except NoSuchElementException:
                fast_del = "This item has no fast delivery"

            price = driver.find_element(By.CSS_SELECTOR, 'span.price-value').text
            price = price.replace('\n', '.')
            currency = driver.find_element(By.CSS_SELECTOR, 'span.price-currency').text
            brand = driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/div[1]/div/main/section/div[3]/div/div/div/div[4]/ul/li[4]/a').text
            Country_del = "This item is made in Bulgaria"

            print(f"{title}, {brand}, {price}, {currency}, {exp_pr}, {fast_del}, {Country_del}")

            writer.writerow([f"Продукт №{product_index + 1}"])
            writer.writerow([title])
            writer.writerow([brand])
            writer.writerow([f"{price} {currency}"])
            writer.writerow([exp_pr])
            writer.writerow([f"Линк към продукта: {product_url}"])
            writer.writerow([fast_del])
            writer.writerow([Country_del])
            writer.writerow([])  # Blank line for separation

            if len(driver.window_handles) > 1:
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                time.sleep(1)

        except StaleElementReferenceException:
            print(f"Element {product_index} is stale, re-fetching the list.")
        except Exception as e:
            print(f"Error processing item {product_index + 1}: {e}")

    driver.quit()
