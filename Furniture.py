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

#extract furniture in url
def feature_extract(url,malicious):
        Feature=defaultdict(list)
	requests.packages.urllib3.disable_warnings()
        tokens_words=re.split('\W+',url)       #Extract bag of words stings delimited by (.,/,?,,=,-,_)
	soup =""
	r=''
	try:
		
		r= requests.get(url,verify=False,timeout=10)
		if 'HTML document' in magic.from_buffer(r.content) :
		     soup=BeautifulSoup(r.content,"lxml")
		#else:
		     #print "request not html"
		     #return -1

	except Exception as e:
		#print "url is die"
		#return -1
		pass
	
        obj=urlparse(url)
	hostname=''
	path=''
	if obj.netloc == '':
	     hostname=obj.path
             path=''
	else:
	     hostname=obj.netloc
	     path=obj.path
        
	query=obj.query
	subdomain,domain,suffix=tldextract.extract(url)

	Feature['URL'].append(url)
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
	#Feature['DomainInSubdomains'].append(DomainInSubdomains(subdomain,suffix))
	Feature['DomainInPath'].append(DomainInPath(path))
	Feature['HttpsInPath'].append(HttpsInPath(path))
	Feature['HostnameLength'].append(HostnameLength(hostname))
	Feature['PathLength'].append(PathLength(path))
	Feature['QueryLength'].append(QueryLength(query))
	Feature['DoubleSlashInPath'].append(DoubleSlashInPath(path))
	Feature['NumSensitiveWords'].append(NumSensitiveWords(tokens_words))
	rank_host,rank_country=rank(hostname)
        Feature['rank_host'].append(rank_host)
	Feature['rank_country'].append(rank_country)
	Feature['AgeDomain'].append(AgeDomain(hostname))
	Feature['Statistical_report'].append(Statistical_report(url,IP))
	Feature['PctExtHyperlinks'].append(PctExtHyperlinks(url, soup, domain))
	Feature['PctExtResourceUrls'].append(PctExtResourceUrls(url, soup, domain))
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
	Feature['PctExtResourceUrlsRT'].append(PctExtResourceUrlsRT(url,soup,domain))
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


#print feature_extract("http://c.img001.com/re58",1)
def search_in_google(url): 

	for j in search(url, tld="co.in", num=10, stop=1, pause=2): 
    		if url in tldextract.extract(j).netloc:
			return j
		else:
			return 0
	return 0

#url="stainupurworejo.ac.id/wp-content/upgrade/autodhl/authorize/track.php?rand=13InboxLightaspxn.1774256418&&email="

#print re.search("^http",url)
#def main(url):
#	if search_in_google(url) ==0:
#		print "url is die"
#	else :
#		url =search_in_google(url)

#	feature_extract(url)
##print "http://facebook.com?x=80".split(':')[1].isdigit()


