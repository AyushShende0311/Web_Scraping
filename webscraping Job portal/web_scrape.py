from bs4 import BeautifulSoup
import requests
import csv

csv_file = open('data.csv', 'w',newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Company Name','Skills required', 'Location', 'Job link'])

for page_number in range(0,5):
    url = requests.get(f'https://www.timesjobs.com/candidate/job-search.html?from=submit&actualTxtKeywords=Data%20Scientist,Machine%20Learning&searchBy=0&rdoOperator=OR&searchType=personalizedSearch&luceneResultSize=25&postWeek=60&txtKeywords=data%20scientist,machine%20learning&cboWorkExp1=0&pDate=I&sequence={page_number}&startPage=1').text
    soup = BeautifulSoup(url,'lxml')
    jobs = soup.findAll('li',class_ = 'clearfix job-bx wht-shd-bx')
    for job in jobs:
        published_date = job.find('span', class_='sim-posted').span.text
        if 'few' in published_date or 'today' in published_date:
            comp_name = job.find('h3',class_='joblist-comp-name').text.replace(' ','').strip()
            # print(f'company name : {comp_name}')
            skills = job.find('span',class_='srp-skills').text.replace(' ','').strip()
            # print(f'skills : {skills}')
            link = job.header.h2.a['href']
            # print(f"Job Link: {link}")
            loc = job.find('ul',class_='top-jd-dtl clearfix')
            for li in loc.find_all('li'):
                if li.span == None:
                    continue
                location = li.span.text
                # print(f'location: {location}')
            csv_writer.writerow([comp_name,skills,location,link])

csv_file.close()