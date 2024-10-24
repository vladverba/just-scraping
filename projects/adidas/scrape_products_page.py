from curl_cffi import requests
import csv
import time
import random


# create a new session with impersonate chrome
def new_session():

    return requests.Session(impersonate="chrome")


# get the products from the url
def get_adidas_url(url: str, session: requests.Session):

    response = session.get(url)
    response.raise_for_status()

    products_list = response.json()["pageProps"]["products"]

    return products_list


# run the scraper
def run_adidas_product_scrape(api_url: str, num_pages: int):
    """
    Sample URL: https://www.adidas.com/plp-app/_next/data/Oqsng-b4i0FabaBWA6C3c/us/men-shoes.json?path=us&taxonomy=men-shoes
    """

    # get taxonomy from api_url
    taxonomy = api_url.split("taxonomy=")[1]

    # make a list urls with start incremented by 48
    urls = [f"{api_url}&start={i * 48}" for i in range(num_pages)]

    session = new_session()

    for url in urls:

        print(f"Scraping {url}")

        output = get_adidas_url(url, session)

        for product in output:

            product_data = {
                "id": product["id"],
                "modelNumber": product["modelNumber"],
                "title": product["title"],
                "url": "https://www.adidas.com" + product["url"],
                "price": product["priceData"]["price"],
                "salePrice": product["priceData"]["salePrice"],
                "discount": product["priceData"]["discountText"],
            }

            # write product to csv
            with open(f"projects/adidas/{taxonomy}.csv", "a+") as f:
                writer = csv.DictWriter(f, fieldnames=product_data.keys())
                if f.tell() == 0:
                    writer.writeheader()
                writer.writerow(product_data)

        time.sleep(random.randint(5, 10))


if __name__ == "__main__":

    run_adidas_product_scrape(
        "https://www.adidas.com/plp-app/_next/data/7l9PYLwzqRWE8hPYy7XD7/us/men-shoes.json?path=us&taxonomy=men-shoes",
        20,
    )
