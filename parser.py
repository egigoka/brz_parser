from bs4 import BeautifulSoup
from commands import Str, File, Network, Print, Time, Random, Threading, q, newline
from models import ProductsPage, Product, Item

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import (ElementClickInterceptedException, TimeoutException,
                                        ElementNotInteractableException)

SLEEP_BETWEEN_ACTIONS = 3
SLEEP_BETWEEN_BACKGROUND_ACTIONS = 1


def sleep_random(seconds, variability_percent=50, verbose=False):
    time_to_sleep = seconds * (100 + Random.integer(-variability_percent, variability_percent)) / 100
    Time.sleep(time_to_sleep, verbose=verbose)


def process_products_page(url_to_process, page_number):

    print(f"start processing products page {page_number}")

    response = Network.get(url_to_process, )
        
    product_page = ProductsPage()

    product_page.page_number = page_number
    product_page.link = url_to_process

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

            current_product = Product()
            current_product.link = product_full_url
            current_product.name = product_name

            product_page.products.append(current_product)

    print(f"finish processing products page {page_number}")
    return product_page
            

def process_product_page(product_to_process):
    print(f"start processing product page")
    # response = Network.get(product.link)
    # html_text = response.text

    # debug DELETE
    product_to_process.link = "https://breezy.kz/smartphone/apple-iphone-12-pro-max-128-gb-pacific-blue-mgda3"
    # debug DELETE
    
    html_text, codes = get_hydrated_page_from_selenium(product_to_process.link, product_page=True)

    soup = BeautifulSoup(html_text, 'html.parser')

    product_name = soup.find("h1", class_="title")

    print(f"product name: {product_name}")

    items_divs = soup.find_all('div', class_='offers__list')

    print(f"{len(items_divs)=}")

    for items_div_cnt, items_div in enumerate(items_divs):
        print(f"\tprocessing {items_div_cnt}th item from product")
        current_item = Item()
        if items_div_cnt > 0:
            raise ValueError("This div should be the only one")

        item_lis = items_div.find_all('li', class_='offers__item offer')

        print(f"{len(item_lis)=}")
        for item_li in item_lis:

            price = item_li.find("div", class_="main price__main")

            current_item.price = price.text.strip()

            print(f"\t{price.text}")

        current_item.code = codes[items_div_cnt]

        product_to_process.items.append(current_item)
        print(f"\tfinish processing {items_div_cnt}th item from product")

    print(f"finish processing product page")

    return product_to_process


def process_item_page(item_to_process):
    print(f"start processing item page")
    print(f"not implemented")
    print(f"finish processing item page")
    return item_to_process


def close_jivo_site(driver):
    Print.rewrite()
    print("trying to close jivo site")
    while True:
        try:
            element = WebDriverWait(driver, 10).until(
                ec.element_to_be_clickable((By.ID, 'jivo_close_button'))
            )
            element.click()

            break  # Exit the loop once the element is clicked
        except TimeoutException:
            pass
    Print.rewrite()
    print("successfully closed jivo site")


def click_with_retries(element, name):
    clicked = False
    while not clicked:
        try:
            print(f"trying to click {name}")
            element.click()
            clicked = True
        except (ElementClickInterceptedException, ElementNotInteractableException) as e:
            print(f"fuck. this. shit. error while clicking {name}: {e}")
            sleep_random(SLEEP_BETWEEN_BACKGROUND_ACTIONS)


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

    while True:
        elements = driver.find_elements(By.CLASS_NAME, 'more__container')

        if len(elements) == 0:
            break

        print(f'found {len(elements)} more buttons, clicking dem al\'')
        for element_cnt, element in enumerate(elements):
            print(f"clicking {element_cnt}st MOAR BUTTAN")
            element.click()
            sleep_random(SLEEP_BETWEEN_ACTIONS, verbose=True)

    elements = driver.find_elements(By.CLASS_NAME, 'offers__list')

    codes = {}
    
    for element_cnt, element in enumerate(elements):
        # li_elements = element.find_elements(By.TAG_NAME, 'li')
        li_elements = element.find_elements(By.XPATH, '*')
        print(f"found {len(li_elements)} li elements with items")
        for li_cnt, li in enumerate(li_elements):
            sleep_random(SLEEP_BETWEEN_ACTIONS, verbose=True)
            print(f"found {li_cnt}th li element, clicking")
            driver.execute_script('arguments[0].scrollIntoView();', li)
            scroll_up_amount = Random.integer(-50, -100)
            print(f"scroll up by {scroll_up_amount}")
            driver.execute_script(f'window.scrollBy(0, {scroll_up_amount});')
            click_with_retries(li, f"{li_cnt}th li element")
            sleep_random(SLEEP_BETWEEN_ACTIONS, verbose=True)

            possible_codes = driver.find_elements(By.CLASS_NAME, 'code_val')

            code = None
            for possible_code in possible_codes:
                if possible_code.text:
                    if possible_code.text.strip() != "":
                        code = possible_code.text
            if code is None:
                raise ValueError(f"Found not exactly 1 code: found {len(possible_codes)}")

            codes[li_cnt] = code
            
            print(f"closing popup")
            # Find the element with both class names
            close_popup_element = driver.find_element(By.CSS_SELECTOR, '.modal_close_icon.modal_close')
            click_with_retries(close_popup_element, "popup")
            sleep_random(SLEEP_BETWEEN_ACTIONS, verbose=True)
            scroll_down_amount = Random.integer(400, 600)
            print(f"scroll down by {scroll_down_amount}")
            driver.execute_script(f'window.scrollBy(0, {scroll_down_amount});')

            print("codes")
            for cnt, code in codes.items():
                print(Str.leftpad(cnt, 2, " "), code)
            print("codes end")

    print(codes)

    t.kill()
    Time.sleep(60, verbose=True)

    return codes
    

def get_hydrated_page_from_selenium(url_to_hydrate, product_page=False):

    # Set up Chrome options
    chrome_options = Options()
    # Use the following line if you want to run Chrome in headless mode (without a visible browser window)
    # chrome_options.add_argument('--headless')

    # Create a WebDriver instance
    driver = webdriver.Chrome(options=chrome_options)

    # Load the URL
    driver.get(url_to_hydrate)

    # Wait for JavaScript to finish executing (adjust the timeout as needed)
    timeout = 60  # in seconds
    wait = WebDriverWait(driver, timeout)
    # wait.until(EC.presence_of_element_located((By.XPATH, '//element-you-want-to-wait-for')))
    # wait.until(EC.presence_of_element_located((By.XPATH, '//body[@status="complete"]')))
    wait.until(lambda selenium_driver: selenium_driver.execute_script("return document.readyState === 'complete';"))

    codes = None
    if product_page:
        codes = get_additional_product_page_info(driver)

    # Retrieve the hydrated HTML content
    html_hydrated_text = driver.page_source

    # Close the browser
    driver.quit()

    if codes:
        return html_hydrated_text, codes
    else:
        return html_hydrated_text

# chrome_driver_path = Path.combine(Path.get_parent(Path.safe__file__(__file__)),
#                                  "chromedriver",
#                                  "chromedriver114.0.5735.90")
# print(chrome_driver_path)


print("let's get this goin'")

url, paged_url, _ = Str.nl(File.read("url.txt"))

domain = Network.get_domain_of_url(url)

products_pages = []
products = []
items = []

next_page = True
current_page = 0
while next_page:
    current_page += 1
    page_url = url if current_page == 1 else paged_url.replace("{{page}}", current_page)

    products_page = process_products_page(page_url, current_page)

    for product_cnt, product in enumerate(products_page.products):
    
        product = process_product_page(product)

        print(f"{len(product.items)=}")

        for item_cnt, item in enumerate(product.items):
            item = process_item_page(item)

            product.items[item_cnt] = item
            print(item)
            items.append(item)

        products_page.products[product_cnt] = product
        products.append(product)
        break

    products_pages.append(products_page)

    next_page = False
    
q = q  # fucking pycharm
