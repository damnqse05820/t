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
from googlesearch import search 

#extract furniture in url
def feature_extract(url,malicious):
        Feature={}
        tokens_words=re.split('\W+',url)       #Extract bag of words stings delimited by (.,/,?,,=,-,_)
	soup=''
	try:
		r= requests.get(url)
		soup=BeautifulSoup(r.content,"lxml")	
	except:
		pass	
        obj=urlparse(url)
        hostname=obj.netloc
        path=obj.path
	query=obj.query
	subdomain,domain,suffix=tldextract.extract(url)
	host=domain+"."+suffix
	Feature['NumDots']=NumDots(url)
	Feature['SubdomainLevel']=SubdomainLevel(subdomain)
	Feature['PathLevel']=PathLevel(path)
        Feature['NumDash']=NumDash(url)
	Feature['NumDashInHost']=NumDashInHostname(hostname)
	Feature['AtSymbol']=AtSymbol(url)
	Feature['TildeSymbol']=TildeSymbol(url)
	Feature['NumUnderscore']=NumUnderscore(url)
	Feature['NumPercent']=NumPercent(url)
	Feature['NumQueryComponents']=NumQueryComponents(query)
	Feature['NumAmpersand']=NumAmpersand(url)
	Feature['NumHash']=NumHash(url)
	Feature['NumNumericChars']=NumNumericChars(url)
	Feature['NoHttps']=NoHttps(url)
	Feature['RandomString']=RandomString(url)
	Feature['IpAddress'],IP = IpAddress(hostname)
	Feature['DomainInSubdomains']= DomainInSubdomains(subdomain,suffix)
	Feature['DomainInPaths']= DomainInPath(path,suffix)
	Feature['HttpsInHostname']= HttpsInHostname(hostname)
	Feature['HostnameLength']=HostnameLength(hostname)
	Feature['DomainInPaths']= DomainInPath(path,suffix)
	Feature['PathLength']= PathLength(path)
	Feature['QueryLength']= QueryLength(query)
	Feature['DoubleSlashInPath']=DoubleSlashInPath(path)
	Feature['NumSensitiveWords']= NumSensitiveWords(tokens_words)
        Feature['rank_host'],Feature['rank_country'] =rank(hostname)
	print IP
	Feature['AgeDomain']= AgeDomain(host)
	Feature['Statistical_report']= Statistical_report(url,IP)
	Feature['PctExtHyperlinks']= PctExtHyperlinks(url, soup, domain)
	Feature['PctExtResourceUrls']=PctExtResourceUrls(url, soup, domain)
	Feature['RightClickDisabled']=RightClickDisabled(soup)
	Feature['PopUpWindow']=PopUpWindow(soup)
	Feature['IframeOrFrame']=IframeOrFrame(soup)
	Feature['SubmitInfoToEmail']=SubmitInfoToEmail(soup)
	Feature['ExtFavicon']=ExtFavicon(url, soup, domain)
        Feature['UrlLength']=UrlLength(url)
	Feature['PctExtNullSelfRedirectHyperlinksRT']=PctExtNullSelfRedirectHyperlinksRT(soup)
	Feature['MissingTitle']=MissingTitle(soup)
	Feature['ImagesOnlyInForm']=ImagesOnlyInForm(soup)
	Feature['SubdomainLevelRT']=SubdomainLevelRT(subdomain)
	Feature['UrlLengthRT']=UrlLengthRT(url)
	Feature['AbnormalExtFormActionR']=AbnormalExtFormActionR(soup)      
	Feature['RelativeFormAction']=RelativeFormAction(soup)
	Feature['ExtMetaScriptLinkRT']=ExtMetaScriptLinkRT(url,soup,domain)
        Feature['AbnormalFormAction']=AbnormalFormAction(soup)
	Feature['PctExtResourceUrlsRT']=PctExtResourceUrlsRT(url,soup,domain) 			    	
        Feature['avg_domain_token_length'],Feature['domain_token_count'],Feature['largest_domain'] = Tokenise(hostname)
        Feature['avg_path_token'],Feature['path_token_count'],Feature['largest_path'] = Tokenise(path)
	Feature['avg_token_length'],Feature['token_count'],Feature['largest_token'] = Tokenise(url)
        Feature['URL']=url
	Feature['Malicious']=malicious
        wfeatures=web_content_features(url)
        
        for key in wfeatures:
            Feature[key]=wfeatures[key]

	Feature['FakeLinkInStatusBar']=FakeLinkInStatusBar(soup)
	Feature['FrequentDomainNameMismatch']=FrequentDomainNameMismatch(domain,soup)
	Feature['PctNullSelfRedirectHyperlinks']=PctNullSelfRedirectHyperlinks(soup)
        return Feature


def search_in_google(url): 
	for j in search(url, tld="co.in", num=10, stop=1, pause=2): 
    		return j
	return 0

url="http://stainupurworejo.ac.id/wp-content/upgrade/autodhl/authorize/track.php?rand=13InboxLightaspxn.1774256418&&email="
print search_in_google(url)

#def main(url):
#	if search_in_google(url) ==0:
#		print "url is die"
#	else :
#		url =search_in_google(url)

#	feature_extract(url)
print(feature_extract(url,0))

