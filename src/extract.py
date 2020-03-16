from selenium.common.exceptions import NoSuchElementException
url= "https://koko.by/cat?postType=listing&postsPerPage=20"
from selenium import webdriver

from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())

res=[]
res1=[]
res3=[]
x=5

page=driver.get(url)
for i in range(10):
    res=driver.find_element_by_tag_name("article")
    res1.append(res)
    i+=1



for link in res1:
    h2= driver.find_element_by_tag_name("h2").get_attribute("innerText")
    res3.append(h2)


print(res3)