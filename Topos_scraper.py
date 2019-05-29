# -*- coding: utf-8 -*-
"""
This program takes URL page as input and creates data file for each of the restaurant listed in the URL page
Created on Sat Nov  3 16:56:17 2018

@author: Team 3
"""

from selenium import webdriver
import time
import requests
import string
import re

city_data_link = 'http://www.city-data.com/city/'

def addl_city_info(city,state):
    
    driver = webdriver.Chrome('chromedriver.exe')
    
    city = city.split('[')[0]
    
    if city == 'New York City':
        city = " ".join(city.split(" ")[:2])
        
    
    if city == 'Washington, D.C.':
        city = city.split(",")[0]
        
    if city == 'Nashville':
        city = 'Nashville-Davidson'
    elif city == 'Lexington':
        city = 'Lexington-Fayette'
    elif city == 'Saint Paul':
        city = 'St.-Paul'
    elif city == 'Boise':
        city = 'Boise-City'
        
    if '–' in city:
        city=city.replace('–','-')
    
    city = city.strip()
    state = state.strip()
    
    print(city)
    print(state)
           
    line = city_data_link + city + '-' + state + '.html'
    
    line = re.sub(' +', '-', line)
    
    print(line)
    
    try:
        driver.get(line)
    except:
        print('No URLs')
    
    try:    
        mal_pct = driver.find_element_by_xpath("""//*[@id="population-by-sex"]/div/table/tbody/tr[1]/td[2]""")
        mpct = mal_pct.text.replace("(","").replace("(","").replace("%","").replace(")","").split(" ")[1]
    except:
        mpct = ''
        print("No Male Percent!")
    
    try:
        fml_pct = driver.find_element_by_xpath("""//*[@id="population-by-sex"]/div/table/tbody/tr[2]/td[2]""")
        fpct = fml_pct.text.replace("(","").replace("(","").replace("%","").replace(")","").split(" ")[1]
    except:
        fpct = ''
        print("No female percent!")
    
    try:
        age = driver.find_element_by_xpath("""//*[@id="median-age"]/div/table/tbody/tr[1]/td[2]""")
        mage = age.text.split(" ")[1]
    except:
        mage = ''
        print("No age info!")
    
    try:
        med_income = driver.find_element_by_xpath("""//*[@id="median-income"]/div[1]/table/tbody/tr[1]/td[2]""")
        minc = med_income.text.replace("$","").replace(",","")
    except:
        minc = ''
        print("No median income info!")
    
    try:
        house_val = driver.find_element_by_xpath("""//*[@id="median-income"]/div[2]/table/tbody/tr[1]/td[2]""")
        hval = house_val.text.replace("$","").replace(",","")
    except:
        hval = ''
        print("No house value info!")
    
    driver.quit()
    
    return mpct, fpct, mage, minc, hval
      

def run(line,driver):
    
    f=open('city_details_add.csv','w', encoding='utf-8-sig') # output file
    
    columnTitleRow = "2018 rank, City, State, 2018 Estimate, 2010 Census, Change(%), 2016 land area(sq mi), 2016 land area(sq km), 2016 population density(sq mi), 2016 population density(sq km), location, Male(%), Female(%), Median Age (yrs), Median Household income ($), Median Household value ($) \n"
    f.write(columnTitleRow)
	        
    try:
        driver.get(line)
    except:
        print('No URLs')
    
    #restaurant name
    
    for i in range(23,25):
        
        try:    
            city = driver.find_element_by_xpath("""//*[@id="mw-content-text"]/div/table[5]/tbody/tr["""+str(i)+"""]/td[2]/i/a""")
        except:
            try:
                city = driver.find_element_by_xpath("""//*[@id="mw-content-text"]/div/table[5]/tbody/tr["""+str(i)+"""]/td[2]/i/b/a""")
            except:
                try:
                    city = driver.find_element_by_xpath("""//*[@id="mw-content-text"]/div/table[5]/tbody/tr["""+str(i)+"""]/td[2]/a""")
                except:
                    try:
                        city = driver.find_element_by_xpath("""//*[@id="mw-content-text"]/div/table[5]/tbody/tr["""+str(i)+"""]/td[2]""")
                    except:    
                        print("No cities found!")
                        break
        
        try:            
            state = driver.find_element_by_xpath("""//*[@id="mw-content-text"]/div/table[5]/tbody/tr["""+str(i)+"""]/td[3]/a""")
        except:
            try:
                state = driver.find_element_by_xpath("""//*[@id="mw-content-text"]/div/table[5]/tbody/tr["""+str(i)+"""]/td[3]""")
            except:
                print("No states found!")
                break
                
            
        try:
            cen_2018 = driver.find_element_by_xpath("""//*[@id="mw-content-text"]/div/table[5]/tbody/tr["""+str(i)+"""]/td[4]""")
        except:
            print("No census 2018 info!")
            
        try:
            cen_2010 = driver.find_element_by_xpath("""//*[@id="mw-content-text"]/div/table[5]/tbody/tr["""+str(i)+"""]/td[5]""")
        except:
            print("No census 2010 info!")
            
            
        try:
            change = driver.find_element_by_xpath("""//*[@id="mw-content-text"]/div/table[5]/tbody/tr["""+str(i)+"""]/td[6]/span[2]""")
        except:
            try:
                change = driver.find_element_by_xpath("""//*[@id="mw-content-text"]/div/table[5]/tbody/tr["""+str(i)+"""]/td[6]""")
            except:
                print("No change!")
                break
        
        #print(change.text) 
        chg_text = change.text
        
        if "NA" in change.text:
            chg_text = change.text.replace(change.text,"NA")
        print(chg_text)
             
    
        la_2016_mi = driver.find_element_by_xpath("""//*[@id="mw-content-text"]/div/table[5]/tbody/tr["""+str(i)+"""]/td[7]""")
    
        la_2016_km = driver.find_element_by_xpath("""//*[@id="mw-content-text"]/div/table[5]/tbody/tr["""+str(i)+"""]/td[8]""")
    
        pd_2016_mi = driver.find_element_by_xpath("""//*[@id="mw-content-text"]/div/table[5]/tbody/tr["""+str(i)+"""]/td[9]""")
    
        pd_2016_km = driver.find_element_by_xpath("""//*[@id="mw-content-text"]/div/table[5]/tbody/tr["""+str(i)+"""]/td[10]""")
    
        location = driver.find_element_by_xpath("""//*[@id="mw-content-text"]/div/table[5]/tbody/tr["""+str(i)+"""]/td[11]""") 
        
        mpct, fpct, mage, minc, hval = addl_city_info(city.text,state.text)
        
        row = str(i)+ "," + city.text.replace(",", "").split("[",1)[0]+ "," + state.text+ "," + cen_2018.text.replace(",", "")+ "," + cen_2010.text.replace(",", "")+ "," + chg_text.replace("%", "").replace("−","-") + "," + la_2016_mi.text.replace(",", "").split(" ",1)[0]+ "," + la_2016_km.text.replace(",", "").split(" ",1)[0]+ \
                "," + pd_2016_mi.text.replace(",", "").split("/",1)[0]+ "," + pd_2016_km.text.replace(",", "").split("/",1)[0]+ "," + location.text \
                + "," + mpct+ "," + fpct + "," + mage + "," + minc + "," + hval + "\n"
        
        
        f.write(row)
        
    f.close()
    
if __name__=='__main__':
    #i=0

    driver = webdriver.Chrome('chromedriver.exe')
    line = 'https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population'
    run(line,driver)
    driver.quit()
        

