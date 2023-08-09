import requests
from bs4 import BeautifulSoup
from commands import Str, File, Network, Console, Print, Path, Time, Random, Threading, q
from models import ProductsPage, Product, Item

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementClickInterceptedException

def process_products_page(page_url, page_number):

    response = Network.get(page_url)
        
    product_page = ProductsPage()

    product_page.page_number = page_number
    product_page.link = page_url

    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all <div> elements with the class "product_list_item product"
    product_divs = soup.find_all('div', class_='product_list_item product')

    for div_cnt, div in enumerate(product_divs):
        # print(div_cnt, div)
        product_a_s = div.find_all("a", class_="product_name")
        for product_a_cnt, product_a in enumerate(product_a_s):
            product_link = product_a['href']
            product_name = product_a.text
            
            product_full_url = f"https://{domain}{product_link}"

            product = Product()
            product.link = product_full_url
            product.name = product_name

            product_page.products.append(product)
            
    return product_page
            

def process_product_page(product):

    # response = Network.get(product.link)
    # html_text = response.text

    product.link = "https://breezy.kz/smartphone/apple-iphone-12-pro-max-128-gb-pacific-blue-mgda3" # debug DELETE
    
    html_text = get_hydrated_page_from_selenium(product.link, product_page=True)

    print(html_text)

    soup = BeautifulSoup(html_text, 'html.parser')

    items_divs = soup.find_all('div', class_='offers__list')


    print(f"{len(items_divs)=}")

    for items_div_cnt, items_div in enumerate(items_divs):
        if items_div_cnt > 0:
            raise ValueError("This div should be the only one")

        item_lis = items_div.find_all('li', class_='offers__item offer')

        print(f"{len(item_lis)=}")
        for item_li in item_lis:

            price = item_li.find("div", class_="main price__main")
            
            print(price.text)
    
    
    return product

def process_item_page(item):
    return item

def close_jivo_site(driver):
    while True:
        try:
            Print.rewrite()
            print("trying to close jivo site")
            element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'jivo_close_button'))
            )
            element.click()
            Print.rewrite()
            print("closed jivo site")
            break  # Exit the loop once the element is clicked
        except Exception as e:
            # print(f"Error: {e}\n while closing jivo site")
            continue  # Retry if there's an error


def click_with_retries(element, name):
    clicked = False
    while not clicked:
        try:
            print(f"trying to click {name}")
            element.click()
            clicked = True
        except ElementClickInterceptedException as e:
            print(f"fuck. this. shit. error while clicking {name}: {e}")


def get_additional_product_page_info(driver):

    t = Threading()
    t.add(close_jivo_site, args=([driver]))
    t.start()
    
    # Find all elements with class "tab_head_link"
    elements = driver.find_elements(By.CLASS_NAME, 'tab_head_link')

    print(f"finding element from {len(elements)=}")
    # Filter the elements based on the "data-tab" attribute
    desired_element = None
    for element in elements:
        data_tab = element.get_attribute('data-tab')
        print(f"found element with {data_tab=}")
        if data_tab == 'offers':
            desired_element = element
            break
    
    if desired_element:
        print("yay!")
        # Do something with the desired element, like clicking or reading info
        desired_element.click()
    else:
        print("nay :(")

    elements = driver.find_elements(By.CLASS_NAME, 'offers__list')

    for element in elements:
        li_elements = element.find_elements(By.TAG_NAME, 'li')
        for li_cnt, li in enumerate(li_elements):
            Time.sleep(10, verbose=True)
            print(f"found {li_cnt}th li element, clicking")
            driver.execute_script('arguments[0].scrollIntoView();', li)
            scroll_up_amount = Random.integer(-50, -100)
            print(f"scroll up by {scroll_up_amount}")
            driver.execute_script(f'window.scrollBy(0, {scroll_up_amount});')
            click_with_retries(li, f"{li_cnt}th li element")
            Time.sleep(10, verbose=True)

            print("NEEED TO GET ID HERE!!!!!!!!!")
            raise NotImplementedError
            
            print(f"closing popup")
            # Find the element with both class names
            close_popup_element = driver.find_element(By.CSS_SELECTOR, '.modal_close_icon.modal_close')
            click_with_retries(close_popup_element, "popup")
            Time.sleep(10, verbose=True)
            scroll_down_amount = Random.integer(400, 600)
            print(f"scroll down by {scroll_down_amount}")
            driver.execute_script(f'window.scrollBy(0, {scroll_down_amount});')
            Time.sleep(10, verbose=True)
    
    Time.sleep(60)
    

def get_hydrated_page_from_selenium(url, product_page=False):

    # Set up Chrome options
    chrome_options = Options()
    # Use the following line if you want to run Chrome in headless mode (without a visible browser window)
    # chrome_options.add_argument('--headless')

    # Create a WebDriver instance
    driver = webdriver.Chrome(options=chrome_options)

    # Load the URL
    driver.get(url)

    # Wait for JavaScript to finish executing (adjust the timeout as needed)
    timeout = 60  # in seconds
    wait = WebDriverWait(driver, timeout)
    #wait.until(EC.presence_of_element_located((By.XPATH, '//element-you-want-to-wait-for')))
    #wait.until(EC.presence_of_element_located((By.XPATH, '//body[@status="complete"]')))
    wait.until(lambda driver: driver.execute_script("return document.readyState === 'complete';"))

    if product_page:
        get_additional_product_page_info(driver)

    # Retrieve the hydrated HTML content
    html_hydrated_text = driver.page_source

    # Close the browser
    driver.quit()
    
    return html_hydrated_text

#chrome_driver_path = Path.combine(Path.get_parent(Path.safe__file__(__file__)), 
#                                  "chromedriver",
#                                  "chromedriver114.0.5735.90")
# print(chrome_driver_path)

url, paged_url, _ = Str.nl(File.read("url.txt"))

domain = Network.get_domain_of_url(url)

products_pages = []
products = []
items = []

next_page = True
current_page = 0
while next_page:
    current_page += 1
    page_url = url if current_page == 1 else paged_url.replace("{{page}}", page)

    products_page = process_products_page(page_url, current_page)

    for product_cnt, product in enumerate(products_page.products):
    
        product = process_product_page(product)

        for item_cnt, item in enumerate(product.items):
            item = process_item_page(item)

            product.items[item_cnt] = item
            items.append(item)

        products_page.products[product_cnt] = product
        products.append(product)
        break

    products_pages.append(products_page)

    next_page = False
    
