import whois
from datetime import datetime
import time

def AgeDomain(domain):# year
    try:
    	domain= whois.query(domain)
	
    except:
	return 0
    if domain==None:
	return 0
    creation_date = domain.creation_date
    expiration_date = domain.expiration_date
    ageofdomain = 0
    if expiration_date:
 	ageofdomain = abs((expiration_date - creation_date).days)
    return ageofdomain / 30

def rank(host):
        xmlpath='http://data.alexa.com/data?cli=10&dat=snbamz&url='+host
	rank_country=-1
	rank_host=-1
        #print xmlpath
        try:
	    r=request.get(xmlpath)
	    rlist=r.content.split('>')
	    for i in rlist:
		if 'REACH' in i and 'RANK=' in i:
		    rank_host=i.split("\"")[-2]
            	if 'COUNTRY' in i and 'RANK=' in i:
		    rank_country=i.split("\"")[-2]
            return [rank_host,rank_country]

        except Exception as e:
            return [-1,-1]


