from selenium import webdriver
from selenium.webdriver import ActionChains
import time
import csv

chromedriver= '/Users/levhotylev/Desktop/chromedrv/chromedriver'

csv_date = []

def write_to_csv():
    resault = open('resault.csv', 'w')
    with resault:
        write = csv.writer(resault)
        write.writerows(csv_date)


def getPre_Open():

    csv_date.append(['Name','Price'])
    driver = webdriver.Chrome()
    driver.get("https://www.nseindia.com ")
    time.sleep(2)
    driver.delete_all_cookies()
    el1 = driver.find_element_by_link_text("MARKET DATA")
    time.sleep(1)
    hover = ActionChains(driver).move_to_element(el1)
    hover.perform()
    el2 = driver.find_element_by_link_text('Pre-Open Market')
    time.sleep(1)
    el2.click()
    time.sleep(12)
    x = driver.find_element_by_xpath('/html/body/div[7]/section/div/h1').text
    table = driver.find_element_by_xpath('/html/body/div[7]/div/section/div/div/div/div/div/div/div[3]/div/table[1]/tbody')
    rows = table.find_elements_by_tag_name("tr")
    for row in rows:
        elemnt_of_rows = row.find_elements_by_tag_name('td')
        obj = [elemnt_of_rows[1].text, elemnt_of_rows[6].text]
        csv_date.append(obj)
        print()

    print('csv_data', csv_date)
    write_to_csv()
    print('--')
    header = driver.find_element_by_xpath('/html/body/header/nav/div[1]/a')
    time.sleep(1)
    driver.delete_all_cookies()
    header.click()
    time.sleep(2)
    move_to_el = driver.find_element_by_xpath('/html/body/div[7]/div[1]/section[9]/div/div/div[1]/div/div[2]/div/div[2]/h5')
    ActionChains(driver).move_to_element(move_to_el).perform()
    print('11')
    driver.close()

getPre_Open()