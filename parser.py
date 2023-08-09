import requests
from bs4 import BeautifulSoup
from commands import Str, File

# Send a GET request to the website
url, paged_url = Str.nl(File.read("url.txt"))

next_page = True
current_page = 0
while next_page:
    current_page += 1
    if page == 1:
        response = requests.get(url)
    else:
        response = requests.get(paged_url.replace("{{page}}", page))

    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all <div> elements with the class "product_list_item product"
    product_divs = soup.find_all('div', class_='product_list_item product')

    # Print the found elements
    for div in product_divs:
        print(div)
    next_page = False
