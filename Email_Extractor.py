import requests
from lxml import html
import pandas as pd
from bs4 import BeautifulSoup


def parseEmail(web):
    allLinks = [];mails=[]
    url = web
    allLinks.append(url)
    path_aboutpages="//a[contains(@href,'about')]/@href"
    path_contactpages="//a[contains(@href,'contacts')]/@href"
    try:
        res=requests.get('http://www.'+url, timeout=2)
    except Exception as e:
        print(e)
        return
    statuscode=res.status_code
    if statuscode in [523, 503, 502, 500, 410, 409, 404]:
        return
    try:
        aboutpages=html.fromstring(res.content).xpath(path_aboutpages)
        contactpages=html.fromstring(res.content).xpath(path_contactpages)
    except Exception as e:
        print(e)
        return
    if aboutpages:
        for i in aboutpages[:3]:
            allLinks.append(i)
    if contactpages:
        for i in contactpages[:3]:
            allLinks.append(i)

    allLinks=set(allLinks)

    def findMails(soup):
        for name in soup.find_all('a'):
            if(name is not None):
                emailText=name.text
                match=bool(re.match('[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',emailText))
                if('@' in emailText and match==True):
                    emailText=emailText.replace(" ",'').replace('\r','')
                    emailText=emailText.replace('\n','').replace('\t','')
                    if(len(mails)==0)or(emailText not in mails):
                        print(emailText)
                    mails.append(emailText)
    for link in allLinks:
        if(link.startswith("http") or link.startswith("www")):
            try:
                r=requests.get(link,timeout=2)
                data=r.text
                soup=BeautifulSoup(data,'html.parser')
                findMails(soup)
            except Exception as e:
                print(e)
                continue

        else:
            try:
                newurl=url+link
                r=requests.get('http://www.'+newurl,timeout=2)
                data=r.text
                soup=BeautifulSoup(data,'html.parser')
                findMails(soup)
            except Exception as e:
                print(e)
                continue

    mails=set(mails)
    return mails
first=0
#input file below
with open('andrewsWebs20201028.csv') as f:
    lines=f.read().split('\n')

for line in lines:
    result={}
    # data=line.split(',')
    # uuid=data[0]
    # web=data[1]
    web=line
    emails=parseEmail(web)
    # result['uuid']=uuid
    result['web']=web
    result['emails']=''
    if emails:
        for email in emails:
            result['emails']=result['emails'] + email +'|'
    df=pd.DataFrame([result])
    print(result)
    #output file below
    df.to_csv('export2020-10-28.csv',mode='a',index=0,header=(first==0))
    first+=1
print('-------end----------')
