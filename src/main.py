from typing import Optional

from selenium import webdriver
import re
import requests

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

#chrome_options = Options()
#chrome_options.add_argument("--headless")
driver = webdriver.Chrome(ChromeDriverManager().install())#, options=chrome_options)


def extract_kfc():
    url = "https://www.kfc.by/promo"
    driver.get(url)

    image_list = []
    name_of_discount_list = []
    href_list = []
    text_list = []
    hrefs = []

    pagination = driver.find_elements_by_class_name("pagination")
    for pagin in pagination:
        links = pagin.find_elements_by_css_selector("a")
        for link in links:
            href = link.get_attribute("href")
            href_list.append(href)
            if len(href_list) == 2:
                break

    for pages in href_list:
        driver.get(pages)

        elements_image = driver.find_elements_by_class_name("content-list-item")
        for element in elements_image:
            tag_a = element.find_element_by_tag_name("a")
            href = tag_a.get_attribute("href")
            hrefs.append(href)

    for href in hrefs:

        driver.get(href)

        try:
            element = driver.find_element_by_xpath(
                "/html/body/div[2]/div[2]/div/div/div[1]/img"
            )
            image_src = element.get_attribute("src")
            image_list.append(image_src)

            element = driver.find_element_by_xpath(
                "/html/body/div[2]/div[2]/div/ul/li[3]"
            )
            name_src = element.get_attribute("innerText")
            name_of_discount_list.append(name_src)

            element = driver.find_element_by_xpath(
                "/html/body/div[2]/div[2]/div/div/div[2]/p[2]"
            )
            text_src = element.get_attribute("innerText")
            text_list.append(text_src)

        except NoSuchElementException:
            continue

    for name_of_discount_list, image_list, text_list in zip(
        name_of_discount_list, image_list, text_list
    ):
        response = requests.post(
            "http://skidon.herokuapp.com/api/v1/discount/",
            data={
                "media": image_list,
                "name_of_discount": name_of_discount_list,
                "shop": "KFC",
                "text": text_list,
            },
        )
        print(response.status_code)


def extract_evroopt():
    url = "https://evroopt.by/redprice/vse-tovary-smm/"
    driver.get(url)

    image_list = []
    name_of_discount_list = []

    elements_src = driver.find_element_by_class_name("small-container-1000")
    elements = elements_src.find_elements_by_class_name("aligncenter")

    for element in elements:
        name_of_discount_src = element.get_attribute("alt")
        name_of_discount_list.append(name_of_discount_src)

        image_src = element.get_attribute("src")
        image_list.append(image_src)

    for name_of_discount_list, image_list in zip(name_of_discount_list, image_list):
        response = requests.post(
            "http://skidon.herokuapp.com/api/v1/discount/",
            data={
                "media": image_list,
                "name_of_discount": name_of_discount_list,
                "shop": "Evroopt",
                "text": image_list,
            },
            timeout=1,
        )
        print(response.status_code)


def extract_vitalur():
    url = "https://vitalur.by/actions/all/"
    driver.get(url)

    image_list = []
    name_of_discount_list = []
    price_list = []
    text_list = []

    i = 0
    elements = driver.find_elements_by_tag_name("section")
    for element in elements:
        image = element.find_element_by_tag_name("img")
        image_src = image.get_attribute("src")
        image_list.append(image_src)

        name_of_discount_src = image.get_attribute("alt")
        name_of_discount_list.append(name_of_discount_src)
        try:
            i += 1
            text = element.find_element_by_xpath(
                f"/html/body/div/div/div/div/div/div[2]/article/div[4]/div[1]/article/section[{i}]/div/div[2]/div/div[2]"
            )
            text_src = text.get_attribute("innerText")
            text_list.append(text_src)

            price = element.find_element_by_xpath(
                f"/html/body/div/div/div/div/div/div[2]/article/div[4]/div[1]/article/section[{i}]/div/div[3]"
            )
            price_src = price.get_attribute("innerText")
            price_list.append(price_src)

        except NoSuchElementException:
            continue

    for name_of_discount_list, image_list, text_list, price_list in zip(
        name_of_discount_list, image_list, text_list, price_list
    ):
        response = requests.post(
            "http://skidon.herokuapp.com/api/v1/discount/",
            data={
                "media": image_list,
                "name_of_discount": text_list,
                "shop": "Vitalur",
                "text": name_of_discount_list,
                "price": price_list,
            },
        )
        print(response.status_code)


def extract_korona():
    url = "https://www.korona.by/buisiness/gipermarket-kalvariiskaya/actions/"
    driver.get(url)

    href_list = []
    text_list = []
    href_in_boxs = []
    name_of_discount_list = []
    image_list = []
    element = driver.find_element_by_class_name("modern-page-navigation")
    hrefs = element.find_elements_by_tag_name("a")

    for href in hrefs:
        href_src = href.get_attribute("href")
        href_list.append(href_src)

    def extcract():
        boxs = driver.find_elements_by_class_name("super-deals-item")
        for box in boxs:
            href_in_boxs.append(box.get_attribute("href"))

    extcract()

    for href in href_list[:-1]:
        driver.get(href)
        extcract()

    for href_in in href_in_boxs:
        driver.get(href_in)

        text = driver.find_element_by_class_name("content-section-boundary-main")
        text_src = text.get_attribute("innerText")
        text_list.append(text_src)

        name_of_discount = driver.find_element_by_tag_name("article")
        price=name_of_discount.find_element_by_tag_name("tr")
        name_of_discount_src = price.get_attribute("innerText")
        name_of_discount_list.append(name_of_discount_src)

        image_src_list = driver.find_element_by_class_name("text-guide")
        image = image_src_list.find_element_by_tag_name("img")
        image_src = image.get_attribute("src")
        image_list.append(image_src)

    for name_of_discount_list, image_list, text_list in zip(
        name_of_discount_list, image_list, text_list
    ):
        response = requests.post(
            "http://skidon.herokuapp.com/api/v1/discount/",
            data={
                "media": image_list,
                "name_of_discount": text_list,
                "shop": "Korona",
                "text": name_of_discount_list,
            },
        )
        print(response.status_code)

def extract_gippo():
    url = "https://gippo.by/clients/specoffers/"
    driver.get(url)

    image_list = []

    elements_src=driver.find_element_by_class_name("caroufredsel_wrapper")
    elements=elements_src.find_elements_by_class_name("slide")

    for element in elements:
        image= element.find_element_by_class_name("pic")
        image_src=image.get_attribute("src")
        image_list.append(image_src)

    for image_list in zip(image_list):
        response = requests.post(
            "http://skidon.herokuapp.com/api/v1/discount/",
            data={
                "media": image_list,
                "shop": "Gippo",
                "text": image_list,
            },
        )
        print(response.status_code)

def extract_bigz():
    url = "https://hitdiscount.by/flyer/"
    driver.get(url)

    image_list=[]

    elements=driver.find_elements_by_tag_name("figure")
    for element in elements:
        image=element.find_element_by_tag_name("img")
        image_src=image.get_attribute("src")
        image_list.append(image_src)

    for image_list in zip(image_list):
        response = requests.post(
            "http://skidon.herokuapp.com/api/v1/discount/",
            data={
                "media": image_list,
                "shop": "Hit",
                "text": image_list,
            },
        )
        print(response.status_code)

def extract_koko_post():
    url = "https://koko.by/post"
    driver.get(url)

    href_list=[]

    elements = driver.find_elements_by_class_name("elementor-post__card")
    for element in elements:
        href = element.find_element_by_class_name("elementor-post__thumbnail__link")
        href_src = href.get_attribute("href")
        href_list.append(href_src)

    while True:
        try:
            next=driver.find_element_by_class_name("elementor-pagination")
            next_src=next.find_element_by_class_name("page-numbers.next")
            next_src.click()
            elements=driver.find_elements_by_class_name("elementor-post__card")
            for element in elements:
                href=element.find_element_by_class_name("elementor-post__thumbnail__link")
                href_src=href.get_attribute("href")
                href_list.append(href_src)
        except Exception:
            continue









    # for image_list in zip(image_list):
    #     response = requests.post(
    #         "http://skidon.herokuapp.com/api/v1/discount/",
    #         data={
    #             "media": image_list,
    #             "shop": "Hit",
    #             "text": image_list,
    #         },
    #     )
    #     print(response.status_code)






extract_koko_post()
