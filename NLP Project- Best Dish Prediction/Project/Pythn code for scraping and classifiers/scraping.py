from bs4 import BeautifulSoup
import urllib2
import re
import csv
import itertools

a=''
b=''
restaurants_url=[]
restaurants_name=[]
restaurants_reviews=[]
reviews_poniters=[]

restaurants_url_copy=[]
restaurants_name_copy=[]

#Restaurant URLs extraction
f1 = urllib2.urlopen("https://www.yelp.ca/search?cflt=restaurants&find_loc=Spring+Garden%2C+Halifax%2C+NS")
html1 = f1.read()
f1.close()
soup = BeautifulSoup(html1)
for elem in soup.find_all('a', href=re.compile('.*/biz/(.*?\?)')):
    a=elem['href']
    a = re.sub(r"(.+)", r"https://www.yelp.ca\1", a)
    restaurants_url.append(a)

f2 = urllib2.urlopen("https://www.yelp.ca/search?cflt=restaurants&find_loc=Spring+Garden%2C+Halifax%2C+NS&start=10")
html2 = f2.read()
f2.close()
soup = BeautifulSoup(html2)
for elem in soup.find_all('a', href=re.compile('.*/biz/(.*?\?)')):
    a=elem['href']
    a = re.sub(r"(.+)", r"https://www.yelp.ca\1", a)
    restaurants_url.append(a)

i=0
j=0

#Restaurant name, reviews Extraction
for i in range(len(restaurants_url)):
    reviews_poniters.append(j)
    f3 = urllib2.urlopen(restaurants_url[i])
    html3 = f3.read()
    f3.close()
    soup = BeautifulSoup(html3)
    
    for m in soup.findAll(attrs={'class' : 'biz-page-title embossed-text-white shortenough'}):
        x=m.contents[0].strip()
        restaurants_name.append(x)
  
    for n in soup.findAll(attrs={'class' : 'biz-page-title embossed-text-white'}):
        y=n.contents[0].strip()
        restaurants_name.append(y)
        
    for g in soup.find_all("p", lang="en"):
        z=g.get_text().strip()
        restaurants_reviews.append(z)
        j=j+1

reviews_poniters.append(j)


for p in range(len(reviews_poniters)-1):
    for q in range(reviews_poniters[p],reviews_poniters[p+1]):
        restaurants_url_copy.insert(q, restaurants_url[p])
        restaurants_name_copy.insert(q, restaurants_name[p])

restaurants_url_copy = [r.encode('utf-8') for r in restaurants_url_copy]
restaurants_name_copy = [t.encode('utf-8') for t in restaurants_name_copy]
restaurants_reviews = [u.encode('utf-8') for u in restaurants_reviews]

#Saving all scraped data in a File.
#Please provide the file path below.
with open("Give any path where you want to save scraped data Restaurant Reviews Data Scraped copy.csv", "wb") as file:
    writer = csv.writer(file, delimiter=',')
    for val in itertools.izip(restaurants_url_copy,restaurants_name_copy,restaurants_reviews):
        writer.writerow(val)

