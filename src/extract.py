from selenium.common.exceptions import NoSuchElementException
url= "https://www.kfc.by/promo"
from selenium import webdriver

from selenium.webdriver.common.keys import Keys

from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())
def extract():
    page = driver.get(url)
    image_dict = []
    name_dict = []
    href_dict= []

    pagination=driver.find_elements_by_class_name("pagination")
    for pagin in pagination:
        links=pagin.find_elements_by_css_selector('a')
        for link in links:
            href=link.get_attribute("href")
            href_dict.append(href)

    for pages in href_dict:
        driver.get(pages)

        elements_image=driver.find_elements_by_class_name("content-list-item")
        for element in elements_image:
            image = element.find_element_by_tag_name("img")
            img_src = image.get_attribute("src")
            image_dict.append(img_src)


        elements_name = driver.find_elements_by_class_name("content-list-main")
        for element in elements_name:
            name = element.find_element_by_tag_name("h2")
            name_src = name.get_attribute("innerText")
            name_dict.append(name_src)

    print(name_dict)
    print(image_dict)
    print(href_dict)
    driver.quit()

extract()










