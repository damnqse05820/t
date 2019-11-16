#!/usr/bin/python
# -*- coding: utf-8 -*-
from urlparse import urlparse
import tldextract
from bs4 import BeautifulSoup
import pandas as pd
import re
from Blacklist_Features import *
from Lexical_Features import *
from Content_based_Features import *
from Host_based_Features import *
from Other_Features import *
import magic
from collections import defaultdict
import requests
#from googlesearch import search
import socket
from io import open
#extract furniture in url
def spliturl(url):
        fragment=''
        spltAr = url.split("://")
        i = (0,1)[len(spltAr)>1]
        hostname = spltAr[i].split("?")[0].split('/')[0].split(':')[0]
        hostname=convert_ip_to_host(hostname)
        obj=urlparse(spltAr[i][len(hostname):])
        query=obj.query
	path =obj.path
        if '#' in url:
                fragment=url.split("#")[-1]
        dirlist=[hostname,path,query,fragment]
        return dirlist

def feature_extract(url,malicious):
        Feature=defaultdict(list)
	requests.packages.urllib3.disable_warnings()
        tokens_words=re.split('\W+',url)       #Extract bag of words stings delimited by (.,/,?,,=,-,_)
	soup =""
	r=''
        try:

                r= requests.get(url,verify=False,timeout=5)
                #print r
                #if r.status_code > 500:
                        #return -1
                 #       pass
                if 'HTML document' in magic.from_buffer(r.content) :
                    #try:
                        
                        html=r.content.encode('ascii','ignore')
                        soup = BeautifulSoup(html, 'lxml')
                    #except:
                       # pass
                else:
                     #print "request not html ,warning"
                     pass
        except Exception as e:
                #print e
                #return -1
                pass
        hostname,path,query,fragment=spliturl(url)
       # print hostname,path,query,fragment
        subdomain,domain,suffix=tldextract.extract(url)
        #print subdomain,domain,suffix

        Feature['URL'].append(url)
        Feature['EmbeddedBrandName'].append(EmbeddedBrandName(domain))
        Feature['NumDots'].append(NumDots(url))
        Feature['SubdomainLevel'].append(SubdomainLevel(subdomain))
        Feature['PathLevel'].append(PathLevel(path))
        Feature['NumDash'].append(NumDash(url))
        Feature['NumDashInHost'].append(NumDashInHostname(hostname))
        Feature['AtSymbol'].append(AtSymbol(url))
        Feature['TildeSymbol'].append(TildeSymbol(url))
        Feature['NumUnderscore'].append(NumUnderscore(url))
        Feature['NumPercent'].append(NumPercent(url))
        Feature['NumQueryComponents'].append(NumQueryComponents(query))
        Feature['NumAmpersand'].append(NumAmpersand(url))
        Feature['NumHash'].append(NumHash(url))
        Feature['NumNumericChars'].append(NumNumericChars(url))
        Feature['NoHttps'].append(NoHttps(url))
        #Feature['RandomString'].append(RandomString(url))
        IpAddresses,IP = IpAddress(hostname)
        Feature['IpAddress'].append(IpAddresses)
        Feature['DomainInSubdomains'].append(DomainInSubdomains(subdomain,domain))
        #Feature['rankSubdomain'].append(rankSubdomain(path))
        Feature['HttpsInPath'].append(HttpsInPath(path))
        Feature['HostnameLength'].append(HostnameLength(hostname))
        Feature['PathLength'].append(PathLength(path))
        Feature['QueryLength'].append(QueryLength(query))
        Feature['DoubleSlashInPath'].append(DoubleSlashInPath(path))
        Feature['NumSensitiveWords'].append(NumSensitiveWords(tokens_words))
        rank_host,rank_country=rank(url)
        Feature['rank_host'].append(rank_host)
        Feature['rank_country'].append(rank_country)
        #print hostname
        Feature['AgeDomain'].append(AgeDomain(hostname))
        #Feature['Statistical_report'].append(Statistical_report(url,IP))
        Feature['PctExtHyperlinks'].append(PctExtHyperlinks(url, soup, domain))
        Feature['PctExtResourceUrls'].append(PctExtResourceUrls(url, soup,domain))
        Feature['RightClickDisabled'].append(RightClickDisabled(soup))
        Feature['PopUpWindow'].append(PopUpWindow(soup))
        Feature['IframeOrFrame'].append(IframeOrFrame(soup))
        Feature['SubmitInfoToEmail'].append(SubmitInfoToEmail(soup))
        Feature['ExtFavicon'].append(ExtFavicon(url, soup, domain))
        Feature['UrlLength'].append(UrlLength(url))
        Feature['PctExtNullSelfRedirectHyperlinksRT'].append(PctExtNullSelfRedirectHyperlinksRT(soup))
        Feature['MissingTitle'].append(MissingTitle(soup))
        Feature['ImagesOnlyInForm'].append(ImagesOnlyInForm(soup))
        Feature['SubdomainLevelRT'].append(SubdomainLevelRT(subdomain))
        Feature['UrlLengthRT'].append(UrlLengthRT(url))
        Feature['AbnormalExtFormActionR'].append(AbnormalExtFormActionR(soup))
        Feature['RelativeFormAction'].append(RelativeFormAction(soup))
        Feature['ExtMetaScriptLinkRT'].append(ExtMetaScriptLinkRT(url,soup,domain))
        Feature['AbnormalFormAction'].append(AbnormalFormAction(soup))
        Feature['PctExtResourceUrlsRT'].append(PctExtResourceUrlsRT(url,soup,domain
))
	'''avg_domain_token_length,domain_token_count, largest_domain = Tokenise(hostname)
        Feature['avg_domain_token_length'].append(avg_domain_token_length)
	Feature['domain_token_count'].append(domain_token_count)
	Feature['largest_domain'].append(largest_domain)
	avg_path_token,path_token_count,largest_path= Tokenise(path)
        Feature['avg_path_token'].append(avg_path_token)
	Feature['path_token_count'].append(path_token_count)
	Feature['largest_path'].append(largest_path)
	avg_token_length,token_count,largest_token=Tokenise(url)
	Feature['avg_token_length'].append(avg_token_length)
	Feature['token_count'].append(token_count)
	Feature['largest_token'].append(largest_token)
     '''

        Feature['Malicious'].append(malicious)
        wfeatures=web_content_features(url,soup)

        for key in wfeatures:
            Feature[key].append(wfeatures[key])

        Feature['FakeLinkInStatusBar'].append(FakeLinkInStatusBar(soup))
        Feature['FrequentDomainNameMismatch'].append(FrequentDomainNameMismatch(domain,soup))
        Feature['PctNullSelfRedirectHyperlinks'].append(PctNullSelfRedirectHyperlinks(soup))
        return Feature

#http://fa.com/en/home.html
#print feature_extract("facebook.com:80",1)
#def search_in_google(url): 
#
#	for j in search(url, tld="co.in", num=10, stop=1, pause=2): 
#    		if url in urlparse(j).netloc:
#			return j
#		else:
#			return 0
#	return 0


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

def scanport(domain):
    #url=''
    try:
        ip=''
        if not checkip_type(domain):
                ip=socket.gethostbyname(domain)
        else:
                ip =domain
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #socket.settimeout(5.0)
        if sock.connect_ex((ip, 443)) == 0:
            #print "Port Open"
            sock.close()
            return 1
        elif sock.connect_ex((ip, 80)) == 0:
            sock.close()
            return 0

    except KeyboardInterrupt:
        return -1
    except socket.gaierror:
        return -1
    except socket.error:
        return -1
    return -1

#url='http://18298.url.9xiazaiqi.com/xiaz/BeyondCompare4ä¸“ä¸šç ´è§£ç‰ˆï¼ˆå'
#print feature_extract(url,1)
#print googleSearch('fabook.com')
#url="stainupurworejo.ac.id/wp-content/upgrade/autodhl/authorize/track.php?rand=13InboxLightaspxn.1774256418&&email="
#print search_in_google("fakebook.com")
#print re.search("^http",url)
#def main(url):
#	if search_in_google(url) ==0:
#		print "url is die"
#	else :
#		url =search_in_google(url)

#	feature_extract(url)
##print "http://facebook.com?x=80".split(':')[1].isdigit()
#url="abcnews.go.com/Politics/2010_Elections/Illinois"
#print scanport("abcnews.go.com")
#print feature_extract(url,1)
#print spliturl(url)

