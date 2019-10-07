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

#extract furniture in url
def feature_extract(url,malicious):
        Feature={}
        tokens_words=re.split('\W+',url)       #Extract bag of words stings delimited by (.,/,?,,=,-,_)
	soup =""
	r=''
	try:
		
		r= requests.get(url,verify=False,timeout=10)
		if 'HTML document' in magic.from_buffer(r.content) :
		     soup=BeautifulSoup(r.content,"lxml")	

	except Exception as e:
		pass
	
        obj=urlparse(url)
        hostname=obj.netloc
        path=obj.path
	query=obj.query
	subdomain,domain,suffix=tldextract.extract(url)
	host=domain+"."+suffix
	
	if url.split(':')[1].isdigit():
		Feature['URL']=url.split(':')[0]
	else:
		Feature['URL']=url
	Feature['NumDots']=NumDots(Feature['URL'])
	Feature['SubdomainLevel']=SubdomainLevel(subdomain)
	Feature['PathLevel']=PathLevel(path)
        Feature['NumDash']=NumDash(Feature['URL'])
	Feature['NumDashInHost']=NumDashInHostname(hostname)
	Feature['AtSymbol']=AtSymbol(Feature['URL'])
	Feature['TildeSymbol']=TildeSymbol(Feature['URL'])
	Feature['NumUnderscore']=NumUnderscore(Feature['URL'])
	Feature['NumPercent']=NumPercent(Feature['URL'])
	Feature['NumQueryComponents']=NumQueryComponents(query)
	Feature['NumAmpersand']=NumAmpersand(Feature['URL'])
	Feature['NumHash']=NumHash(url)
	Feature['NumNumericChars']=NumNumericChars(Feature['URL'])
	Feature['NoHttps']=NoHttps(Feature['URL'])
	Feature['RandomString']=RandomString(Feature['URL'])
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
	Feature['AgeDomain']= AgeDomain(host)
	Feature['Statistical_report']= Statistical_report(Feature['URL'],IP)
	Feature['PctExtHyperlinks']= PctExtHyperlinks(Feature['URL'], soup, domain)
	Feature['PctExtResourceUrls']=PctExtResourceUrls(Feature['URL'], soup, domain)
	Feature['RightClickDisabled']=RightClickDisabled(soup)
	Feature['PopUpWindow']=PopUpWindow(soup)
	Feature['IframeOrFrame']=IframeOrFrame(soup)
	Feature['SubmitInfoToEmail']=SubmitInfoToEmail(soup)
	Feature['ExtFavicon']=ExtFavicon(Feature['URL'], soup, domain)
        Feature['UrlLength']=UrlLength(Feature['URL'])
	Feature['PctExtNullSelfRedirectHyperlinksRT']=PctExtNullSelfRedirectHyperlinksRT(soup)
	Feature['MissingTitle']=MissingTitle(soup)
	Feature['ImagesOnlyInForm']=ImagesOnlyInForm(soup)
	Feature['SubdomainLevelRT']=SubdomainLevelRT(subdomain)
	Feature['UrlLengthRT']=UrlLengthRT(Feature['URL'])
	Feature['AbnormalExtFormActionR']=AbnormalExtFormActionR(soup)      
	Feature['RelativeFormAction']=RelativeFormAction(soup)
	Feature['ExtMetaScriptLinkRT']=ExtMetaScriptLinkRT(Feature['URL'],soup,domain)
        Feature['AbnormalFormAction']=AbnormalFormAction(soup)
	Feature['PctExtResourceUrlsRT']=PctExtResourceUrlsRT(Feature['URL'],soup,domain) 			    	
        Feature['avg_domain_token_length'],Feature['domain_token_count'],Feature['largest_domain'] = Tokenise(hostname)
        Feature['avg_path_token'],Feature['path_token_count'],Feature['largest_path'] = Tokenise(path)
	Feature['avg_token_length'],Feature['token_count'],Feature['largest_token'] = Tokenise(Feature['URL'])
       
	Feature['Malicious']=malicious
        wfeatures=web_content_features(url,soup)
        
        for key in wfeatures:
            Feature[key]=wfeatures[key]

	Feature['FakeLinkInStatusBar']=FakeLinkInStatusBar(soup)
	Feature['FrequentDomainNameMismatch']=FrequentDomainNameMismatch(domain,soup)
	Feature['PctNullSelfRedirectHyperlinks']=PctNullSelfRedirectHyperlinks(soup)
        return Feature


#print feature_extract("http://c.img001.com/re58",1)
#def search_in_google(url): 
	
#	if re.search("^http",url):
#		return url
#	for j in search(url, tld="co.in", num=10, stop=1, pause=2): 
#    		if url in j:
#			return j
#		else:
#			return 0
#	return 0

#url="stainupurworejo.ac.id/wp-content/upgrade/autodhl/authorize/track.php?rand=13InboxLightaspxn.1774256418&&email="

#print re.search("^http",url)
#def main(url):
#	if search_in_google(url) ==0:
#		print "url is die"
#	else :
#		url =search_in_google(url)

#	feature_extract(url)
##print "http://facebook.com?x=80".split(':')[1].isdigit()


