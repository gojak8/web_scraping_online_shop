from bs4 import BeautifulSoup
import requests
import pandas as pd

data = {
    'product_name': [],
    'product_code': [],
    'product_categories': [],
    'product_picture': []
}


def entering_product_page(url_product):
    product_request = requests.get(url_product)
    # we want to provide data and to put them in the dictionary named 'data'
    if product_request.status_code == requests.codes.ok:
        product_page = BeautifulSoup(product_request.text, 'html.parser')
        product_name = product_page.find('h1', class_='product_title entry-title').text
        data['product_name'].append(product_name)
        product_code = product_page.find('span', class_='sku')
        if product_code:
            product_code = product_code.text
        else:
            product_code = ''
        data['product_code'].append(product_code)
        categories = product_page.find('a', rel='tag').text
        data['product_categories'].append(categories)
        product_picture = product_page.find('a', class_='ct-image-container ct-lazy')['href']
        data['product_picture'].append(product_picture)
        file = pd.DataFrame(data, columns=['product_name', 'product_code', 'product_categories', 'product_picture'])
        file.to_csv('bazdar.csv', index=False)
    else:
        print('product url was not found')


def entering_catalogue(url_catalogue):
    catalogue_request = requests.get(url_catalogue)
    if catalogue_request.status_code == requests.codes.ok:
        bs = BeautifulSoup(catalogue_request.text, 'html.parser')
        all_products = bs.find_all('li', class_='product')
        # we want to enter the page of every product
        for product in all_products:
            url_product = product.find('a')['href']
            if url_product == '':
                print("product url was not found")
                continue
            else:
                entering_product_page(url_product)
        next_page = bs.find('a', class_='next page-numbers')
        # we want to recursively call 'entering_catalogue' function as long as the 'next_page' of the online shop exists
        if next_page:
            next_page = bs.find('a', class_='next page-numbers')['href']
            print(next_page)
            entering_catalogue(next_page)
    else:
        print(catalogue_request.text)


url_website = 'https://bazdar.rs/prodavnica/'
entering_catalogue(url_website)
