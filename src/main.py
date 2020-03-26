from selenium import webdriver
import requests
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

#chrome_options = Options()
#chrome_options.add_argument("--headless")
driver = webdriver.Chrome(ChromeDriverManager().install())#,options=chrome_options)


def extract_categ():
    url = "https://koko.by/post/"
    for i in range(6):
        page = driver.get(url + f"{i}")
        post_of_categ = driver.find_elements_by_class_name("listing_header__2pt4D is-verified")


def extract_kfc():
    url = "https://www.kfc.by/promo"
    page = driver.get(url)
    image_list = []
    name_of_discount_list = []
    href_list = []
    text_list=[]
    hrefs=[]
    shop_list=[]
    pagination = driver.find_elements_by_class_name("pagination")
    for pagin in pagination:
        links = pagin.find_elements_by_css_selector('a')
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
            href=tag_a.get_attribute("href")

            hrefs.append(href)
    for href in hrefs:
        driver.get(href)
        try:

            element = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/div/div[1]/img")
            image_src=element.get_attribute("src")
            image_list.append(image_src)

            element = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/ul/li[3]")
            name_src = element.get_attribute("innerText")
            name_of_discount_list.append(name_src)

            element = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/div/div[2]/p[2]")
            text_src = element.get_attribute("innerText")
            text_list.append(text_src)

        except NoSuchElementException:
            continue


    for name_of_discount_list, image_list, text_list_list in zip(name_of_discount_list, image_list, text_list):
        response=requests.post("http://skidon.herokuapp.com/api/v1/discount/", data={"media":image_list, "name_of_discount": name_of_discount_list, "shop":"KFC" , "text":text_list})
        print(response.status_code)




extract_kfc()

