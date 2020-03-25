
from selenium import webdriver

from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())

def extract_categ():
    url="https://koko.by/post/"
    for i in range(6):
        page = driver.get(url+f"{i}")
        post_of_categ = driver.find_elements_by_class_name("listing_header__2pt4D is-verified")

def extract_kfc():
    url = "https://www.kfc.by/promo"
    page = driver.get(url)
    image_list = []
    name_list = []
    href_list = []

    pagination = driver.find_elements_by_class_name("pagination")
    for pagin in pagination:
        links = pagin.find_elements_by_css_selector('a')
        for link in links:
            href = link.get_attribute("href")
            href_list.append(href)
            if len(href_list) == 3:
                break

    for pages in href_list:
        driver.get(pages)

        elements_image = driver.find_elements_by_class_name("content-list-item")
        for element in elements_image:
            image = element.find_element_by_tag_name("img")
            img_src = image.get_attribute("src")
            image_list.append(img_src)

        elements_name = driver.find_elements_by_class_name("content-list-main")
        for element in elements_name:
            name = element.find_element_by_tag_name("h2")
            name_src = name.get_attribute("innerText")
            name_list.append(name_src)

    print(name_list)
    print(image_list)



extract_kfc()
extract_categ()
