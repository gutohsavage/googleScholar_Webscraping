from selenium import webdriver

import pandas as pd
import requests as req
from bs4 import BeautifulSoup
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


PATH = "C:\pathja\chromedriver"
driver = webdriver.Chrome(PATH)

user_ID = []
name = []
Affiliation = []


url = 'https://scholar.google.com/citations?view_op=view_org&hl=en&org=10241031385301082500'

rows=[]

driver.get(url)

temp = []
for i in range(30):
    r = req.get(driver.current_url)
    s = BeautifulSoup(r.content, 'html.parser')
    d = s.find_all('div', {'class': 'gsc_1usr'})


    driver.find_element(By.XPATH,'//*[@id="gsc_authors_bottom_pag"]/div/button[2]').click()
    temp = temp + d

for i in temp :


    tt = i.find_all('div', {'class': 'gs_ai_aff'})
    tt = str(tt).split('[<div class="gs_ai_aff">')[1]
    tt = str(tt).split('</div>]')[0]

    user = i.find('a')['href']
    user = str(user).split('/citations?hl=en&user=')[1]
    user_ID.append(user)
    name_tags = i.find_all('h3', {'class': 'gs_ai_name'})
    name_tags = str(name_tags).split('[<h3 class="gs_ai_name"><a href="/citations?hl=en&amp;user='+str(user)+'">')[1]
    name_tags = str(name_tags).split('</a></h3>]')[0]

    rows.append((user,name_tags, tt))

df = pd.DataFrame(rows,columns=['user','name','Affiliation'])
#user_ID = user
print(df)
df.to_csv('Author.csv',index=False)






paper= []
for i in user_ID :

    driver.get("https://scholar.google.com/citations?hl=en&user="+str(i))
    while True:
        try:
            element = WebDriverWait(driver, 1).until(
                EC.element_to_be_clickable((By.ID, 'gsc_bpf_more'))
            )
            element.click()
        except:
            break

    try :
        loopfor= driver.find_element(By.CSS_SELECTOR,"#gsc_a_nn").text
        loop = str(loopfor).split('Articles 1–')[1]
        iloop = int(loop)
    except :
        iloop = 1

    for j in range( 1,iloop+1):
        driver.find_element(By.CSS_SELECTOR,"#gsc_a_b > tr:nth-child(" + str(j) + ") > td.gsc_a_t > a").click()

        time.sleep(2)
        try:
            tittle = driver.find_element(By.CSS_SELECTOR,"#gsc_vcd_title")
            tittles = tittle.text
        except:

            tittles = " "

        try:
            author = driver.find_element(By.CSS_SELECTOR,"#gsc_vcd_table > div:nth-child(1) > div.gsc_vcd_value")
            authors = author.text
        except:
            authors = " "
        try:
            date = driver.find_element(By.CSS_SELECTOR,"#gsc_vcd_table > div:nth-child(2) > div.gsc_vcd_value")
            dates = date.text
            if len(dates) > 11:
                dates = " "
        except:
            dates = " "
        try:
            descrip = driver.find_element(By.CSS_SELECTOR,"#gsc_vcd_descr")
            des = descrip.text
        except:
            des = " "

        driver.find_element(By.CSS_SELECTOR,"#gs_md_cita-d-x > span.gs_ico").click()

        citeby = driver.find_element(By.CSS_SELECTOR,"#gsc_a_b > tr:nth-child(" + str(j) + ") > td.gsc_a_c > a")
        cite = citeby.text

        paper.append((tittles,authors,dates,des,cite))
    time.sleep(3)

df2 = pd.DataFrame(paper,columns=['title','author','publication_date','description','cite_by'])
df2.to_csv('Paper.csv', index=False)







driver.quit()