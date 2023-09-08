from bs4 import BeautifulSoup
from commands import Str, File, Network, Print, Time, Random, Threading, Path, q, newline
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
SLEEP_BEFORE_CLOSING_SELENIUM = 0

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


            possible_photo = item_li.find("div", class_="offer__preview-container")

            if possible_photo is not None:
                current_item.photo = possible_photo.find("img")['src']

            offer__value = item_li.find("span", class_="offer__grade")

            if offer__value is not None:
                current_item.grade_brz = offer__value.text.strip()

            offer__spec = item_li.find("div", class_="offer__spec")

            offer__spec_items = offer__spec.find_all("li", class_="offer__item")

            for offer__spec_item in offer__spec_items:
                offer__spec_item_name = offer__spec_item.find("span", class_="offer__name").text.strip()
                offer__spec_item_value = offer__spec_item.find("span", class_="offer__value")

                if offer__spec_item_name == "Состояние":
                    current_item.grade_brz_verbose = offer__spec_item_value.text.strip()
                elif offer__spec_item_name == "Батарея":
                    current_item.battery_percent = offer__spec_item_value.text.strip()
                elif offer__spec_item_name == "Дефект":
                    current_item.defect = offer__spec_item_value.text.strip()
                elif offer__spec_item_name == "Комплектация":
                    current_item.included = offer__spec_item_value.text.strip()
                elif offer__spec_item_name == "Корпус":
                    current_item.case_state = offer__spec_item_value.text.strip()
                elif offer__spec_item_name == "Дисплей":
                    current_item.display_state = offer__spec_item_value.text.strip()
                elif offer__spec_item_name == "Гарантия":
                    current_item.warranty = offer__spec_item_value.text.strip()
                else:
                    raise ValueError(f"Unknown offer__spec_item_name: {offer__spec_item_name}")

            diagnostic_certificate_link = item_li.find("a", class_="offer__download")

            if diagnostic_certificate_link is not None:
                current_item.certificate_link = diagnostic_certificate_link['href']
            # example: https://diag.nsystools.com/Report/Certificate?AsPDF=True&Imei=356723114035410&loadOldTests=False&isLink=True&clid=4f8a90cc-54e6-4a6d-af7f-f519b859b79c
            current_item.certificate_link = current_item.certificate_link.replace("AsPDF=True", "AsPDF=False")

            diagnostic_certificate_response = Network.get(current_item.certificate_link)

            diagnostic_certificate_html_text = diagnostic_certificate_response.text

            print(f"\t\tfarming diagnostic link {diagnostic_certificate_html_text}")

            diagnostic_certificate_soup = BeautifulSoup(diagnostic_certificate_html_text, 'html.parser')

            diagnostic_certificate_divs = diagnostic_certificate_soup.find_all("div", class_="row")

            for diagnostic_certificate_div in diagnostic_certificate_divs:
                diagnostic_certificate_div_name = diagnostic_certificate_div.find("div", class_="col title")
                diagnostic_certificate_div_value = diagnostic_certificate_div.find("div", class_="col")

                if diagnostic_certificate_div_name is not None and diagnostic_certificate_div_value is not None:
                    if diagnostic_certificate_div_name.text.strip() == "IMEI 1":
                        current_item.imei1 = diagnostic_certificate_div_value.text.strip()
                    elif diagnostic_certificate_div_name.text.strip() == "IMEI 2":
                        current_item.imei2 = diagnostic_certificate_div_value.text.strip()
                    elif diagnostic_certificate_div_name.text.strip() == "SN":
                        current_item.sn = diagnostic_certificate_div_value.text.strip()
                    elif diagnostic_certificate_div_name.text.strip() == "OS Version":
                        current_item.os_version = diagnostic_certificate_div_value.text.strip()
                    elif diagnostic_certificate_div_name.text.strip() == "Build ver":
                        current_item.build_version = diagnostic_certificate_div_value.text.strip()
                    elif diagnostic_certificate_div_name.text.strip() == "Firmware":
                        current_item.firmware = diagnostic_certificate_div_value.text.strip()
                    elif diagnostic_certificate_div_name.text.strip() == "Region info":
                        current_item.region_info = diagnostic_certificate_div_value.text.strip()
                    elif diagnostic_certificate_div_name.text.strip() == "Spec":
                        current_item.spec = diagnostic_certificate_div_value.text.strip()
                    elif diagnostic_certificate_div_name.text.strip() == "Carrier":
                        current_item.carrier = diagnostic_certificate_div_value.text.strip()
                    elif diagnostic_certificate_div_name.text.strip() == "Model":
                        current_item.model = diagnostic_certificate_div_value.text.strip()
                    elif diagnostic_certificate_div_name.text.strip() == "MPN":
                        current_item.mpn = diagnostic_certificate_div_value.text.strip()
                    elif diagnostic_certificate_div_name.text.strip() == "Vendor State":
                        current_item.vendor_state = diagnostic_certificate_div_value.text.strip()
                    elif diagnostic_certificate_div_name.text.strip() == "Last NSYS Tested":
                        current_item.last_nsys_tested = diagnostic_certificate_div_value.text.strip()
                    elif diagnostic_certificate_div_name.text.strip() == "NSYS Certificated":
                        current_item.nsys_certificated = diagnostic_certificate_div_value.text.strip()
                    elif diagnostic_certificate_div_name.text.strip() == "Battery health":
                        current_item.battery_health = diagnostic_certificate_div_value.text.strip()
                    elif diagnostic_certificate_div_name.text.strip() == "Battery cycle":
                        current_item.battery_cycle = diagnostic_certificate_div_value.text.strip()
                    elif diagnostic_certificate_div_name.text.strip() == "FMIP":
                        current_item.fmip = diagnostic_certificate_div_value.text.strip()
                    elif diagnostic_certificate_div_name.text.strip() == "JAIL":
                        current_item.jail = diagnostic_certificate_div_value.text.strip()
                    elif diagnostic_certificate_div_name.text.strip() == "MDM":
                        current_item.mdm = diagnostic_certificate_div_value.text.strip()
                    elif diagnostic_certificate_div_name.text.strip() == "ESN":
                        current_item.esn = diagnostic_certificate_div_value.text.strip()
                    elif diagnostic_certificate_div_name.text.strip() == "ESNA":
                        current_item.esna = diagnostic_certificate_div_value.text.strip()
                    elif diagnostic_certificate_div_name.text.strip() == "SimLock":
                        current_item.simlock = diagnostic_certificate_div_value.text.strip()
                    elif diagnostic_certificate_div_name.text.strip() == "Purchase Date":
                        current_item.purchase_date = diagnostic_certificate_div_value.text.strip()
                    elif diagnostic_certificate_div_name.text.strip() == "CoverageDate":
                        current_item.coverage_date = diagnostic_certificate_div_value.text.strip()
                    elif diagnostic_certificate_div_name.text.strip() == "Supplier":
                        current_item.supplier = diagnostic_certificate_div_value.text.strip()
                    elif diagnostic_certificate_div_name.text.strip() == "Invoice":
                        current_item.invoice = diagnostic_certificate_div_value.text.strip()
                    elif diagnostic_certificate_div_name.text.strip() == "Grade":
                        current_item.grade_nsys = diagnostic_certificate_div_value.text.strip()
                    elif diagnostic_certificate_div_name.text.strip() == "Note":
                        current_item.note = diagnostic_certificate_div_value.text.strip()
                    else:
                        raise ValueError(f"Unknown diagnosic_certificate_div_name: {diagnostic_certificate_div_name.text.strip()}")

            test_results_div = diagnostic_certificate_soup.find_all("li", class_="d-flex justify-content-between list-group-item border-0 mr-3")

            for test_results_div_item in test_results_div:
                test_results_div_item_name = test_results_div_item.find("span").text.strip()
                test_results_div_item_value_image = test_results_div_item.find("img")

                if test_results_div_item_value_image is not None:
                    if test_results_div_item_value_image['src'] == "data:image/svg+xml;base64, PHN2ZyB3aWR0aD0iMjMiIGhlaWdodD0iMjMiIHZpZXdCb3g9IjAgMCAyMyAyMyIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4NCjxnIGNsaXAtcGF0aD0idXJsKCNjbGlwMF8zODA2XzE1MjY4KSI+DQo8cGF0aCBmaWxsLXJ1bGU9ImV2ZW5vZGQiIGNsaXAtcnVsZT0iZXZlbm9kZCIgZD0iTTE5LjgwNTIgNi4xODY4MkMyMC4yMTc4IDYuNjQwNzQgMjAuMTg0NCA3LjM0MzIyIDE5LjczMDUgNy43NTU4N0w5Ljk1NTk3IDE2LjY0MThDOS41Mjc5NCAxNy4wMzA5IDguODcyOTEgMTcuMDI2MyA4LjQ1MDMyIDE2LjYzMTNMMi42NzQ0OCAxMS4yMzIzQzIuMjI2MzQgMTAuODEzNCAyLjIwMjY0IDEwLjExMDUgMi42MjE1NCA5LjY2MjM2QzMuMDQwNDUgOS4yMTQyMiAzLjc0MzMzIDkuMTkwNTIgNC4xOTE0NyA5LjYwOTQzTDkuMjE5MjkgMTQuMzA5MkwxOC4yMzYxIDYuMTEyMTFDMTguNjkgNS42OTk0NiAxOS4zOTI1IDUuNzMyOTEgMTkuODA1MiA2LjE4NjgyWiIgZmlsbD0iIzM3QTA2NCIvPg0KPC9nPg0KPGRlZnM+DQo8Y2xpcFBhdGggaWQ9ImNsaXAwXzM4MDZfMTUyNjgiPg0KPHJlY3Qgd2lkdGg9IjE3Ljc3MTgiIGhlaWdodD0iMTcuNzcxOCIgZmlsbD0id2hpdGUiIHRyYW5zZm9ybT0idHJhbnNsYXRlKDIuMzIyMjQgMi40OTA5NykiLz4NCjwvY2xpcFBhdGg+DQo8L2RlZnM+DQo8L3N2Zz4NCg==":
                        test_results_div_item_value = True
                    else:
                        test_results_div_item_value = False
                else:
                    test_results_div_item_value = None
                if test_results_div_item_name == "Front camera":
                    current_item.front_camera = test_results_div_item_value
                elif test_results_div_item_name == "Back camera":
                    current_item.back_camera = test_results_div_item_value
                elif test_results_div_item_name == "Flash":
                    current_item.flash = test_results_div_item_value
                elif test_results_div_item_name == "TrueDepthCamera":
                    current_item.three_d_touch = test_results_div_item_value
                elif test_results_div_item_name == "Touchscreen":
                    current_item.touchscreen = test_results_div_item_value
                elif test_results_div_item_name == "Vibro":
                    current_item.vibration = test_results_div_item_value
                elif test_results_div_item_name == "Front microphone":
                    current_item.front_microphone = test_results_div_item_value
                elif test_results_div_item_name == "VideoMic":
                    current_item.video_microphone = test_results_div_item_value
                elif test_results_div_item_name == "Bottom mic":
                    current_item.bottom_microphone = test_results_div_item_value
                elif test_results_div_item_name == "Microphone":
                    current_item.microphone = test_results_div_item_value
                elif test_results_div_item_name == "LoudSpeaker":
                    current_item.loud_speaker = test_results_div_item_value
                elif test_results_div_item_name == "Speaker":
                    current_item.speaker = test_results_div_item_value
                elif test_results_div_item_name == "LCDPixels":
                    current_item.lcd_pixels = test_results_div_item_value
                elif test_results_div_item_name == "Barometer":
                    current_item.barometer = test_results_div_item_value
                elif test_results_div_item_name == "Accelerometer":
                    current_item.accelerometer = test_results_div_item_value
                elif test_results_div_item_name == "Compass":
                    current_item.compass = test_results_div_item_value
                elif test_results_div_item_name == "Gyroscope":
                    current_item.gyroscope = test_results_div_item_value
                elif test_results_div_item_name == "Geolocation":
                    current_item.geolocation = test_results_div_item_value
                elif test_results_div_item_name == "Network":
                    current_item.network = test_results_div_item_value
                elif test_results_div_item_name == "Bluetooth":
                    current_item.bluetooth = test_results_div_item_value
                elif test_results_div_item_name == "WiFi":
                    current_item.wifi = test_results_div_item_value
                elif test_results_div_item_name == "Sim Reader":
                    current_item.sim_reader = test_results_div_item_value
                elif test_results_div_item_name == "Proximity":
                    current_item.proximity = test_results_div_item_value
                elif test_results_div_item_name == "Light sensor":
                    current_item.light_sensor = test_results_div_item_value
                elif test_results_div_item_name == "Volume Down":
                    current_item.volume_down = test_results_div_item_value
                elif test_results_div_item_name == "Volume Up":
                    current_item.volume_up = test_results_div_item_value
                elif test_results_div_item_name == "RingSilent button":
                    current_item.ring_silent_button = test_results_div_item_value
                elif test_results_div_item_name == "Face ID":
                    current_item.face_touch_id = test_results_div_item_value
                elif test_results_div_item_name == "MultiTouch":
                    current_item.multi_touch = test_results_div_item_value
                else:
                    raise ValueError(f"Unknown test_results_div_item_name: {test_results_div_item_name}")

            non_original_parts_div = diagnostic_certificate_soup.find("div", class_="non-original-parts")

            parts_divs = non_original_parts_div.find_all("div", class_="row ml-2")

            for parts_div in parts_divs:
                cols = parts_div.find_all("div", class_="col")

                part_name = None
                part_status = None

                for cnt_col, col in enumerate(cols):
                    if cnt_col == 0:
                        span = col.find("span")
                        part_name = span.text.strip()
                    elif cnt_col == 3:
                        part_status = col.text.strip()
                    else:
                        raise ValueError(f"Unknown cnt_col: {cnt_col}")

                if part_name == "Mother board":
                    current_item.is_motherboard_original = part_status
                elif part_name == "Battery":
                    current_item.is_battery_original = part_status
                elif part_name == "Front camera":
                    current_item.is_front_camera_original = part_status
                elif part_name == "Back camera":
                    current_item.is_back_camera_original = part_status
                elif part_name == "Display":
                    current_item.is_display_original = part_status
                elif part_name == "TouchID":
                    current_item.is_touch_id_original = part_status
                elif part_name == "Parts":
                    continue
                else:
                    raise ValueError(f"Unknown part_name: {part_name}")

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
    Time.sleep(SLEEP_BEFORE_CLOSING_SELENIUM, verbose=True)

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
    
print(products_pages[0])
