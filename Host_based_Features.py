import whois
from datetime import datetime
import time
import requests
import socket
import tldextract
import urllib2

#from Furniture import *
def checkip_type(domain):
        if len(domain.split('.'))==4:
                try:
                        for i in domain.split('.'):
                                if int(i)<0 or int(i)>255:
                                        return False
                        return True
                except Exception:
                        return False
        return False
def convert_ip_to_host(ip):
        if checkip_type(ip):
                try:
                        return socket.gethostbyaddr(ip)[0]
                except:
                        return ip
        return ip

def AgeDomain(domain):# year
    try:
        domain =convert_ip_to_host(domain)
       # print domain
        age= whois.query(domain)
        #print age.__dict___
        creation_date = age.creation_date
        #print(creation_date)
        expiration_date = age.expiration_date
        #print(expiration_date)
    except:
        return 0
    ageofdomain = 0
    if expiration_date:
        ageofdomain = abs((expiration_date - creation_date).days)
        #print ageofdomain
    return 1 if ageofdomain/180 > 1 else 0

def rank(host):
        #host=convert_ip_to_host(host)
	
        xmlpath='http://data.alexa.com/data?cli=10&dat=snbamz&url='+host
        rank_country=-1
        rank_host=-1
        #print xmlpath
        try:
            r=requests.get(xmlpath)
            #print r.content
            rlist=r.content.split('>')
            for i in rlist:
                if 'REACH' in i and 'RANK=' in i:
                    if int(i.split("\"")[-2])<10000000:
                        rank_host=1
                if 'COUNTRY' in i and 'RANK=' in i:
                    if int(i.split("\"")[-2])<10000000:
                        rank_country=1
            return [rank_host,rank_country]

        except Exception as e:
            return [-1,-1]
#print rank('https://outlook.office.com/mail/inbox')

def EmbeddedBrandName(domain):
        host=convert_ip_to_host(domain)
        subdomain,domain,suffix=tldextract.extract(host)
        url="https://autocomplete.clearbit.com/v1/companies/suggest?query="+domain+"."+suffix
        response=""
        for i in range(2):
            try:
                req = urllib2.Request(url)
                response = urllib2.urlopen(req)
                break
            except:
                time.sleep(1)
        if response =="":
            the_page =""
        else:
	    the_page = response.read()
	#print the_page
        #r=requests.get(url,verify=False,allow_redirects=True)
        strlist={"name","domain","logo"}
        for i in strlist :
                if i in the_page:
                        return 1
        return 0

#def
#print AgeDomain('daday.vuikhoetainha.com')
#print EmbeddedBrandName('facebook.com')
