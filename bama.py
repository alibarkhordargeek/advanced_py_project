import requests
from bs4 import BeautifulSoup
import re
import mysql.connector
from sklearn import tree

cnm = input('نام خودروی مورد نظر را وارد کنید: ')
cadrs = input('شهر مورد نظر را وارد کنید: ')
cprc = input('محدوده قیمت خودروی مورد نظر را وارد کنید: ')

req = requests.get('https://bama.ir/car/%s/%s?price=%s' %(cnm, cadrs, cprc))
soup = BeautifulSoup(req.text, 'html.parser')

c_name = soup.find_all('p', attrs = {'class': 'bama-ad__title'})
c_age = soup.find_all('div', attrs = {'class': 'bama-ad__detail-row'})
c_address = soup.find_all('div', attrs = {'class': 'bama-ad__address'})
c_price = soup.find_all('div', attrs = {'class': 'bama-ad__price-holder'})

names = list()
ages = list()
addresses = list()
prices = list()

for nm in c_name:
    nm = nm.text.strip()
    names.append(nm)
    
for yr in c_age:
    yr = re.findall(r'\d{4}', yr.text)
    yr = yr[0]
    ages.append(yr)
    
for adrs in c_address:
    adrs = adrs.text.strip()
    addresses.append(adrs)
    
for prc in c_price:
    prc = prc.text.strip()
    prices.append(prc)
    
if len(names) != 0:
    x = list()
    y = list()
    for i in range(0, len(names)):
        x.append([names[i], ages[i]])
        y.append(prices[i])
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(x, y)
    pred_c = input('نام و سن خودروی مورد نظر را وارد کنید: ')
    pred = clf.predict(pred_c)
    print('پیش بینی قیمت: %s' %pred)    
else:
    pass

if len(names) != 0:
    print('مشخصات خودروی مطابق با درخواست شما: ')
    for i in range(0, len(names)):
        print('خودروی: %s سال: %s آدرس: %s قیمت: %s' %(names[i], ages[i], addresses[i], prices[i]))
    cnct = mysql.connector.connect(user='root', password='',
    host='127.0.0.1', database='bama')
    cursor = cnct.cursor()
    for i in range(0, len(names)):
        cursor.execute('insert into cars values (\'%s\', \'%s\', \'%s\', \'%s\')' %(names[i], ages[i], addresses[i], prices[i]))
    cnct.commit()
    cnct.close()
else:
    print('هیچ خودرویی مطابق با درخواست شما پیدا نشد!')
