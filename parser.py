import sys

from bs4 import BeautifulSoup
from commands import Str, File, Network, Print, Time, Random, Threading, JsonDict, Console, Path, Dir, List, q, newline
from models import ProductsPage, Product, Item
from urllib3.exceptions import MaxRetryError

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import (ElementClickInterceptedException, TimeoutException,
                                        ElementNotInteractableException, NoSuchElementException,
                                        StaleElementReferenceException)

q = q  # fuck PyCharm

OUTPUT_FOLDER = "output"
PREVIOUS_FOLDER = "previous"
OUTPUT_TEMP_FOLDER = "output_temp"

HEADLESS = True
FIRST_PAGE = 1
LOAD_PAGES = None
DEBUG = False

for arg in sys.argv:
    if arg.startswith("--first-page="):
        Print.colored(f"First page: {arg}", "red")
        FIRST_PAGE = Str.get_integers(arg)[0]
    elif arg.startswith("--load-pages="):
        Print.colored(f"Load pages: {arg}", "red")
        LOAD_PAGES = Str.get_integers(arg)[0]
    elif arg == "--window":
        Print.colored("Window mode", "red")
        HEADLESS = False
    elif arg == "--debug":
        Print.colored("Debug enabled", "red")
        DEBUG = True

SLEEP_BETWEEN_ACTIONS = 3
SLEEP_BETWEEN_BACKGROUND_ACTIONS = 1
SLEEP_BEFORE_CLOSING_SELENIUM = 0


def sleep_random(seconds, variability_percent=50, verbose=False):
    time_to_sleep = seconds * (100 + Random.integer(-variability_percent, variability_percent)) / 100
    Time.sleep(time_to_sleep, verbose=verbose)


def process_certificate_page(current_item):
    current_item.certificate_link = current_item.certificate_link.replace("AsPDF=True", "AsPDF=False")

    if current_item.certificate_link.strip() == "exists":
        return

    Print.colored(f"\t\t\tfarming diagnostic link {current_item.certificate_link}", "blue")

    diagnostic_certificate_response = Network.get(current_item.certificate_link)

    diagnostic_certificate_html_text = diagnostic_certificate_response.text

    diagnostic_certificate_soup = BeautifulSoup(diagnostic_certificate_html_text, 'html.parser')

    certificate_body = diagnostic_certificate_soup.find("div", id="certificate-body")

    info_div = certificate_body.find_all("div", class_="row")[2]

    diagnostic_certificate_divs = info_div.find_all("div", class_="row")
    if DEBUG:
        print(f"\t\t{len(diagnostic_certificate_divs)=}")
    for diagnostic_certificate_div in diagnostic_certificate_divs:
        diagnostic_certificate_div_name = diagnostic_certificate_div.find("span", class_="col title")
        diagnostic_certificate_div_value = diagnostic_certificate_div.find_all("span", class_="col")[1]

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
                current_item.sim_lock = diagnostic_certificate_div_value.text.strip()
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
                raise ValueError(
                    f"Unknown diagnostic_certificate_div_name: {diagnostic_certificate_div_name.text.strip()}")

    test_results_div = diagnostic_certificate_soup.find("div", class_="test-results")

    try:
        test_results_divs = test_results_div.find_all("li",
                                                      class_="d-flex justify-content-between list-group-item border-0 "
                                                             "mr-3")
    except AttributeError:
        test_results_divs = []

    for test_results_div_item in test_results_divs:
        test_results_div_item_name = test_results_div_item.find("span").text.strip()
        test_results_div_item_value_image = test_results_div_item.find("img")

        if test_results_div_item_value_image is not None:
            if test_results_div_item_value_image['src'] == ("data:image/svg+xml;base64, PHN2ZyB3aWR0aD0iMjMiIGh"  # noqa
                                                            "laWdodD0iMjMiIHZpZXdCb3g9IjAgMCAyMyAyMyIgZmlsbD0ib"  # noqa
                                                            "m9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3Z"  # noqa
                                                            "nIj4NCjxnIGNsaXAtcGF0aD0idXJsKCNjbGlwMF8zODA2XzE1M"  # noqa
                                                            "jY4KSI+DQo8cGF0aCBmaWxsLXJ1bGU9ImV2ZW5vZGQiIGNsaXA"  # noqa
                                                            "tcnVsZT0iZXZlbm9kZCIgZD0iTTE5LjgwNTIgNi4xODY4MkMyM"  # noqa
                                                            "C4yMTc4IDYuNjQwNzQgMjAuMTg0NCA3LjM0MzIyIDE5LjczMDU"  # noqa
                                                            "gNy43NTU4N0w5Ljk1NTk3IDE2LjY0MThDOS41Mjc5NCAxNy4wM"  # noqa
                                                            "zA5IDguODcyOTEgMTcuMDI2MyA4LjQ1MDMyIDE2LjYzMTNMMi4"  # noqa
                                                            "2NzQ0OCAxMS4yMzIzQzIuMjI2MzQgMTAuODEzNCAyLjIwMjY0I"  # noqa
                                                            "DEwLjExMDUgMi42MjE1NCA5LjY2MjM2QzMuMDQwNDUgOS4yMTQ"  # noqa
                                                            "yMiAzLjc0MzMzIDkuMTkwNTIgNC4xOTE0NyA5LjYwOTQzTDkuM"  # noqa
                                                            "jE5MjkgMTQuMzA5MkwxOC4yMzYxIDYuMTEyMTFDMTguNjkgNS4"  # noqa
                                                            "2OTk0NiAxOS4zOTI1IDUuNzMyOTEgMTkuODA1MiA2LjE4NjgyW"  # noqa
                                                            "iIgZmlsbD0iIzM3QTA2NCIvPg0KPC9nPg0KPGRlZnM+DQo8Y2x"  # noqa
                                                            "pcFBhdGggaWQ9ImNsaXAwXzM4MDZfMTUyNjgiPg0KPHJlY3Qgd"  # noqa
                                                            "2lkdGg9IjE3Ljc3MTgiIGhlaWdodD0iMTcuNzcxOCIgZmlsbD0"  # noqa
                                                            "id2hpdGUiIHRyYW5zZm9ybT0idHJhbnNsYXRlKDIuMzIyMjQgM"  # noqa
                                                            "i40OTA5NykiLz4NCjwvY2xpcFBhdGg+DQo8L2RlZnM+DQo8L3N"  # noqa
                                                            "2Zz4NCg=="):  # fucking pycharm
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
        elif test_results_div_item_name == "Face ID" \
                or test_results_div_item_name == "Touch ID":
            current_item.face_touch_id = test_results_div_item_value
        elif test_results_div_item_name == "MultiTouch":
            current_item.multi_touch = test_results_div_item_value
        elif test_results_div_item_name == "3dTouch":
            current_item.three_d_touch = test_results_div_item_value
        elif test_results_div_item_name == "Home button":
            current_item.home_button = test_results_div_item_value
        elif test_results_div_item_name == "TelephotoCamera":
            current_item.telephoto_camera = test_results_div_item_value
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
            elif cnt_col in range(1, 3):
                continue
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


def process_products_page(driver, url_to_process, page_number):
    domain = Network.get_domain_of_url(url_to_process)

    Print.colored(f"start processing products page {page_number}: {url_to_process}", "green")

    response = get_hydrated_page_from_selenium(driver, url_to_process, product_page=False)

    if DEBUG:
        print(f"{len(response)=}")

    product_page = ProductsPage()

    product_page.page_number = page_number
    product_page.link = url_to_process

    soup = BeautifulSoup(response, 'html.parser')

    # Find all <div> elements with the class "product_list_item product"
    product_divs = soup.find_all('div', class_='product_list_item product')

    for div_cnt, div in enumerate(product_divs):
        # print(div_cnt, div)
        product_a_s = div.find_all("a", class_="product_name")
        product_action = div.find("div", class_="product_action")

        if product_action.find("span", class_="text").text.strip() == "Уведомить":
            Print.colored(f"\t{div_cnt}th product is out of stock, breaking processing products page {page_number}",
                          "red")
            break

        for product_a_cnt, product_a in enumerate(product_a_s):
            product_link = product_a['href']
            product_name = product_a.text

            product_full_url = f"https://{domain}{product_link}"

            current_product = Product()
            current_product.link = product_full_url
            current_product.name = product_name

            product_page.products.append(current_product)

    Print.colored(f"finish processing products page {page_number}", "green")
    return product_page


def process_product_page(driver, product_to_process):
    Print.colored(f"\tstart processing product page {product_to_process.link}", "blue")
    # response = Network.get(product.link)
    # html_text = response.text

    html_text, additional_info = get_hydrated_page_from_selenium(driver, product_to_process.link, product_page=True)

    soup = BeautifulSoup(html_text, 'html.parser')

    # product_name = soup.find("h1", class_="title")
    #
    # print(f"product name: {product_name}")

    items_divs = soup.find_all('div', class_='offers__list')

    if DEBUG:
        print(f"{len(items_divs)=}")

    for items_div_cnt, items_div in enumerate(items_divs):

        if DEBUG:
            Print.debug(f"items_div = {items_div}")

        retry = 0
        max_retry = 10
        is_empty = False
        while True:
            retry += 1
            if len(items_div.find_all()) == 0:
                if retry > max_retry:
                    Print.colored(f"\t\t{items_div_cnt}th items div is empty", "red")
                    is_empty = True
                    break
                else:
                    sleep_random(SLEEP_BETWEEN_BACKGROUND_ACTIONS)
                    continue
        if is_empty:
            continue

        if items_div_cnt > 0:
            raise ValueError("This div should be the only one")

        item_lis = items_div.find_all('li', class_='offers__item offer')

        if DEBUG:
            print(f"{len(item_lis)=}")
        for item_li_cnt, item_li in enumerate(item_lis):

            Print.colored(f"\t\tprocessing {item_li_cnt}th item from product", "blue")

            current_item = Item()

            price = item_li.find("div", class_="main price__main")
            price_text = price.text

            price_text = price_text.replace(newline, "\t")
            price_text = price_text.strip("\t")
            price_text = price_text.replace(" ", "")
            price_text = price_text.replace("\t₸", "₸")
            while "\t\t" in price_text:
                price_text = price_text.replace("\t\t", "\t")

            current_item.price = price_text

            current_item.name = product_to_process.name

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

            if current_item.certificate_link is not None:
                process_certificate_page(current_item)

            if DEBUG:
                Print.debug(f"current_item = {current_item}")

            # TODO: something wrong here? need to parse selenium info item by item?

            current_item.code = additional_info[item_li_cnt]["code"]
            current_item.photo = additional_info[item_li_cnt]["picture"]
            current_item.capacity = additional_info["capacity"]

            product_to_process.items.append(current_item)

            Print.colored(f"\t\tfinish processing {item_li_cnt}th item from product", "blue")

    Print.colored(f"\tfinish processing product page", "blue")

    return product_to_process


def close_jivo_site(driver):
    Print.rewrite()
    if DEBUG:
        print("trying to close jivo site")
    while True:
        try:
            element = WebDriverWait(driver, 10).until(
                ec.element_to_be_clickable((By.ID, 'jivo_close_button'))
            )
            element.click()

            break  # Exit the loop once the element is clicked
        except (TimeoutException, MaxRetryError):
            pass
    Print.rewrite()
    if DEBUG:
        print("successfully closed jivo site")


def click_with_retries(element, name):
    retry = 0
    max_retries = 10
    clicked = False
    while not clicked:
        retry += 1
        try:
            if DEBUG:
                print(f"trying to click {name}")
            element.click()
            clicked = True
        except (ElementClickInterceptedException, ElementNotInteractableException) as e:
            print(f"error while clicking {name}: {e}")
            if retry > max_retries:
                raise e
            sleep_random(SLEEP_BETWEEN_BACKGROUND_ACTIONS)


def get_additional_product_page_info(driver):
    additional_info = {}

    site_content = driver.find_element(By.CLASS_NAME, 'site_content')
    product_page = site_content.find_element(By.CLASS_NAME, 'product-page')
    info__content = product_page.find_element(By.CLASS_NAME, 'info__content')
    info__info = info__content.find_element(By.CLASS_NAME, 'info__info')
    if DEBUG:
        Print.debug(f'{info__info.get_attribute("innerHTML")=}')

    retry = 0
    max_retry = 10
    price = None
    while True:
        retry += 1

        try:
            price = info__info.find_element(By.CLASS_NAME, 'price')
            break  # successfully found element
        except NoSuchElementException:
            if retry < max_retry:
                sleep_random(SLEEP_BETWEEN_BACKGROUND_ACTIONS, verbose=True)
                continue
            else:
                Console.blink()
                raise

    if price is None:
        raise ValueError("cannot find element 'price'")
    else:
        if DEBUG:
            Print.debug(f"price.text.strip() = {price.text.strip()}")
        no_stock = len(price.find_elements(By.CLASS_NAME, 'price-no-stock'))
        if DEBUG:
            Print.debug(f"{no_stock=}")
            Print.debug(f'{price.get_attribute("innerHTML")=}')
        if no_stock or price.text.strip() == "Товар закончился":
            return additional_info

    t = Threading()
    t.add(close_jivo_site, args=([driver]))
    t.start()

    # Find capacity
    # Find all elements with class "tab_head_link"
    elements = driver.find_elements(By.CLASS_NAME, 'tab_head_link')

    if DEBUG:
        print(f"finding element from {len(elements)=}")
    # Filter the elements based on the "data-tab" attribute
    element_to_find = 'characteristics'
    retry = 0
    max_retries = 10
    while True:
        retry += 1
        desired_element = None
        for element in elements:
            data_tab = element.get_attribute('data-tab')
            if DEBUG:
                print(f"found element with {data_tab=}")
            if data_tab == element_to_find:
                desired_element = element
                break  # successfully found element

        if desired_element:
            if DEBUG:
                print(f"Found desired element {element_to_find}")
            # Do something with the desired element, like clicking or reading info
            desired_element.click()
            break  # successfully clicked element
        else:
            if retry > max_retries:
                raise KeyError("Cannot find desired element with data-tab = offers")
            else:
                sleep_random(SLEEP_BETWEEN_BACKGROUND_ACTIONS, verbose=True)

    description__row_divs = driver.find_elements(By.CLASS_NAME, 'description__row')

    for description__row in description__row_divs:
        description__row_name = description__row.find_element(By.CLASS_NAME, 'description__name')
        description__row_value = description__row.find_element(By.CLASS_NAME, 'description__value')
        if description__row_name.text.strip() == "Внутренняя память":
            additional_info["capacity"] = description__row_value.text.strip()
            break  # successfully found element

    # Find all elements with class "tab_head_link"
    elements = driver.find_elements(By.CLASS_NAME, 'tab_head_link')

    if DEBUG:
        print(f"finding element from {len(elements)=}")
    # Filter the elements based on the "data-tab" attribute
    element_to_find = 'offers'
    retry = 0
    max_retries = 10
    while True:
        retry += 1
        desired_element = None
        for element in elements:
            data_tab = element.get_attribute('data-tab')
            if DEBUG:
                print(f"found element with {data_tab=}")
            if data_tab == element_to_find:
                desired_element = element
                break  # successfully found element

        if desired_element:
            if DEBUG:
                print(f"Found desired element {element_to_find}")
            # Do something with the desired element, like clicking or reading info
            desired_element.click()
            break  # successfully clicked element
        else:
            if retry > max_retries:
                raise KeyError("Cannot find desired element with data-tab = offers")
            else:
                sleep_random(SLEEP_BETWEEN_BACKGROUND_ACTIONS, verbose=True)

    while True:
        elements = driver.find_elements(By.CLASS_NAME, 'more__container')

        if len(elements) == 0:
            if DEBUG:
                print("no MOAR buttons found")
            break  # nothing to search further

        if DEBUG:
            print(f'found {len(elements)} MOAR buttons, clicking dem al\'')
        for element_cnt, element in enumerate(elements):
            if DEBUG:
                print(f"clicking {element_cnt}st MOAR button")
            element.click()
            sleep_random(SLEEP_BETWEEN_ACTIONS, verbose=True)

    elements = driver.find_elements(By.CLASS_NAME, 'offers__list')

    for element_cnt, element in enumerate(elements):
        # li_elements = element.find_elements(By.TAG_NAME, 'li')
        li_elements = element.find_elements(By.XPATH, '*')
        if DEBUG:
            print(f"found {len(li_elements)} li elements with items")
        for li_cnt, li in enumerate(li_elements):
            sleep_random(SLEEP_BETWEEN_ACTIONS, verbose=True)
            if DEBUG:
                print(f"found {li_cnt}th li element, clicking")
            driver.execute_script('arguments[0].scrollIntoView();', li)
            scroll_up_amount = Random.integer(-50, -100)
            if DEBUG:
                print(f"scroll up by {abs(scroll_up_amount)}")
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

            retry = 0
            max_retries = 10
            picture_link = None
            while True:
                retry += 1
                picture_swiper_slides = driver.find_elements(By.CLASS_NAME, 'swiper-slide')
                picture_swiper_slide = picture_swiper_slides[-1]
                picture_swiper_slide_img = picture_swiper_slide.find_element(By.TAG_NAME, 'img')
                try:
                    picture_link = picture_swiper_slide_img.get_attribute('src')
                    break  # successfully found element
                except StaleElementReferenceException:
                    if retry < max_retries:
                        sleep_random(SLEEP_BETWEEN_BACKGROUND_ACTIONS, verbose=True)
                        continue
                    else:
                        raise

            additional_info[li_cnt] = {"code": code, "picture": picture_link}

            if DEBUG:
                print(f"closing info popup")
            # Find the element with both class names
            close_popup_element = driver.find_element(By.CSS_SELECTOR, '.modal_close_icon.modal_close')
            click_with_retries(close_popup_element, "popup")
            sleep_random(SLEEP_BETWEEN_ACTIONS, verbose=True)
            scroll_down_amount = Random.integer(400, 600)
            if DEBUG:
                print(f"scroll down by {scroll_down_amount}")
            driver.execute_script(f'window.scrollBy(0, {scroll_down_amount});')

            # print("codes")
            # for cnt, code in additional_info.items():
            #     print(Str.leftpad(cnt, 2, " "), code)
            # print("codes end")

    # print(additional_info)

    t.kill()
    Time.sleep(SLEEP_BEFORE_CLOSING_SELENIUM, verbose=True)

    return additional_info


def get_hydrated_page_from_selenium(driver, url_to_hydrate, product_page=False):
    # Load the URL
    retry = 0
    max_retries = 10
    while True:
        retry += 1
        try:
            driver.get(url_to_hydrate)
            break  # successfully loaded page
        except MaxRetryError:
            if retry < max_retries:
                sleep_random(SLEEP_BETWEEN_BACKGROUND_ACTIONS, verbose=True)
                continue
            else:
                raise

    # Wait for JavaScript to finish executing (adjust the timeout as needed)
    timeout = 60  # in seconds
    wait = WebDriverWait(driver, timeout)
    wait.until(lambda selenium_driver: selenium_driver.execute_script("return document.readyState === 'complete';"))

    if product_page and driver.current_url != url_to_hydrate:
        raise ValueError(f"URL mismatch: {driver.current_url} != {url_to_hydrate}")

    additional_info = {}
    if product_page:
        additional_info = get_additional_product_page_info(driver)

    # Retrieve the hydrated HTML content
    html_hydrated_text = driver.page_source

    if product_page:
        return html_hydrated_text, additional_info
    else:
        return html_hydrated_text


def main():
    Print.colored("Start processing", "green")

    url, paged_url, _ = Str.nl(File.read("url.txt"))

    products_pages = []
    products = []
    items = []

    # Set up Chrome options
    chrome_options = Options()
    if HEADLESS:
        chrome_options.add_argument('--headless')

    # Create a WebDriver instance
    driver = webdriver.Chrome(options=chrome_options)

    current_page = 0
    while True:
        current_page += 1

        if current_page < FIRST_PAGE:
            continue  # skip pages
        elif LOAD_PAGES:
            if current_page >= (FIRST_PAGE + LOAD_PAGES):
                Print.colored(f"Loaded {LOAD_PAGES} pages as asked, exiting", "green")
                break  # we've loaded enough pages

        page_url = url if current_page == 1 else paged_url.replace("{{page}}", str(current_page))

        try:
            products_page = process_products_page(driver, page_url, current_page)
        except ValueError as e:
            Print.colored(f"ValueError while processing products page {current_page}, exiting" + newline + e, "red")
            break  # no more pages with products

        if len(products_page.products) == 0:
            Print.colored(f"Loaded {current_page} page, no products inside, exiting", "green")
            break  # no more pages with products

        if DEBUG:
            print()
            print(f"{products_page.page_number=}")
            print(f"{products_page.link=}")
            print(f"{len(products_page.products)=}")
            # print(f"{products_page.products[0]=}")
            # print(f"{products_page.products[-1]=}")
            print()

        for product_cnt, product in enumerate(products_page.products):

            product = process_product_page(driver, product)

            if DEBUG:
                print(f"{len(product.items)=}")

            for item_cnt, item in enumerate(product.items):
                items.append(item)

            products_page.products[product_cnt] = product
            products.append(product)

        products_pages.append(products_page)

    # Close the browser
    driver.quit()

    # diffing

    if not Dir.exists(OUTPUT_TEMP_FOLDER):
        Dir.create(OUTPUT_TEMP_FOLDER)
    if not Dir.exists(OUTPUT_FOLDER):
        Dir.create(OUTPUT_FOLDER)
    if not Dir.exists(PREVIOUS_FOLDER):
        Dir.create(PREVIOUS_FOLDER)

    Dir.cleanup(OUTPUT_TEMP_FOLDER)

    if DEBUG:
        Print.debug("saving products")
    for product in products:
        if DEBUG:
            Print.debug(f"\tsaving product {product.name}")
        output = JsonDict(Path.combine(".", OUTPUT_TEMP_FOLDER, f"{product.name}.json"))
        output.clear()
        for item in product.items:
            if DEBUG:
                Print.debug(f"\t\tsaving item {item.code} {item.imei1} {item.imei2}")
            output[item.code] = item.dict()
        output.save()

    previous_folder = PREVIOUS_FOLDER
    if Dir.list_of_files(OUTPUT_FOLDER):
        # if previous diff failed
        previous_folder = OUTPUT_FOLDER

    files = Dir.list_of_files(previous_folder) + Dir.list_of_files(OUTPUT_TEMP_FOLDER)

    files = List.remove_duplicates(files)

    print("<<DIFF START>>")

    for file in files:
        current_json = JsonDict(Path.combine(".", OUTPUT_TEMP_FOLDER, file))
        previous_json = JsonDict(Path.combine('.', previous_folder, file))

        for code_current, item_current in current_json.items():

            item_name = current_json.filename.replace(File.get_extension(current_json.filename), '')
            item_name = item_name.replace(Path.get_parent(item_name), "")
            item_name += ' ' + code_current

            something_changed = False

            if code_current in previous_json.keys():
                # run diff on sub elements
                for key, current_value in item_current.items():
                    try:
                        previous_value = previous_json[code_current][key]
                    except KeyError:
                        previous_value = None
                    if current_value != previous_value:
                        print(
                            f'In item {item_name} value {key} was changed from "{previous_value}" to "{current_value}"')
                        something_changed = True
            else:
                print(f'New item {item_name} was added: {item_current}')
                something_changed = True
            if something_changed:
                print()

        for code_previous, item_previous in previous_json.items():
            item_name = previous_json.filename.replace(File.get_extension(previous_json.filename), '')
            item_name = item_name.replace(Path.get_parent(item_name), "")
            item_name += ' ' + code_previous

            if code_previous not in current_json.keys():
                # it's deleted
                print(f'Item {item_name} was deleted')
                print()

    print("<<DIFF END>>")

    Print.colored(f"Total products pages: {len(products_pages)}", "green")
    Print.colored(f"Total products: {len(products)}", "green")
    Print.colored(f"Total items: {len(items)}", "green")

    # finished comparing without issues
    Dir.delete(PREVIOUS_FOLDER)
    Dir.move(OUTPUT_FOLDER, PREVIOUS_FOLDER)
    Dir.move(OUTPUT_TEMP_FOLDER, OUTPUT_FOLDER)


if __name__ == '__main__':
    main()
