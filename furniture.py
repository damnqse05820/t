from urlparse import urlparse
import re
import urllib2
import urllib
from xml.dom import minidom
import csv
import tldextract
import socket
import requests
from bs4 import BeautifulSoup
import pandas as pd

opener = urllib2.build_opener()
print opener
opener.addheaders = [('User-agent', 'Mozilla/5.0')]

nf=-1

def Tokenise(url):

        if url=='':
            return [0,0,0]
        token_word=re.split('\W+',url)
        #print token_word
        no_ele=sum_len=largest=0
        for ele in token_word:
                l=len(ele)
                sum_len+=l
                if l>0:                                        ## for empty element exclusion in average length
                        no_ele+=1
                if largest<l:
                        largest=l
        try:
            return [float(sum_len)/no_ele,no_ele,largest]
        except:
            return [0,no_ele,largest]


def find_ele_with_attribute(dom,ele,attribute):
    for subelement in dom.getElementsByTagName(ele):
        if subelement.hasAttribute(attribute):
            return subelement.attributes[attribute].value
    return nf
        

def rank(host):

        xmlpath='http://data.alexa.com/data?cli=10&dat=snbamz&url='+host
        #print xmlpath
        try:
            xml= urllib2.urlopen(xmlpath)
            dom =minidom.parse(xml)
            rank_host=find_ele_with_attribute(dom,'REACH','RANK')
            #country=find_ele_with_attribute(dom,'REACH','RANK')
            rank_country=find_ele_with_attribute(dom,'COUNTRY','RANK')
            return [rank_host,rank_country]

        except:
            return [nf,nf]


def Security_sensitive(tokens_words):

    sec_sen_words=['confirm', 'account', 'banking', 'secure', 'ebayisapi', 'webscr', 'login', 'signin']
    cnt=0
    for ele in sec_sen_words:
        if(ele in tokens_words):
            cnt+=1;

    return cnt



def Check_IPaddress(url):
    try:
	IP=socket.gethostbyname(url)
	return 1,IP
    except:
	return 0
    
def PctNullSelfRedirectHyperlinks(soup):
    count=0
    total=0
    for link in soup.find_all('link', href=True):
	if link['href']=='' or link['href']=='#':
		count+=1
	total+=1
    
    try:
        percentage = count / float(total) * 100
	return percentage
    except:
        return 1


def web_content_features(url):#search cac the 
    wfeatures={}
    total_cnt=0
    try:        
        source_code = str(opener.open(url))
        #print source_code[:500]

        wfeatures['src_html_cnt']=source_code.count('<html')
        wfeatures['src_hlink_cnt']=source_code.count('<a href=')
        wfeatures['src_iframe_cnt']=source_code.count('<iframe')
        #suspicioussrc_ javascript functions count

        wfeatures['src_eval_cnt']=source_code.count('eval(')
        wfeatures['src_escape_cnt']=source_code.count('escape(')
        wfeatures['src_link_cnt']=source_code.count('link(')
        wfeatures['src_underescape_cnt']=source_code.count('underescape(')
        wfeatures['src_exec_cnt']=source_code.count('exec(')
        wfeatures['src_search_cnt']=source_code.count('search(')
        
        for key in wfeatures:
            if(key!='src_html_cnt' and key!='src_hlink_cnt' and key!='src_iframe_cnt'):
                total_cnt+=wfeatures[key]
        wfeatures['src_total_jfun_cnt']=total_cnt
    
    except Exception, e:
        print "Error"+str(e)+" in downloading page "+url 
        default_val=nf
        
        wfeatures['src_html_cnt']=default_val
        wfeatures['src_hlink_cnt']=default_val
        wfeatures['src_iframe_cnt']=default_val
        wfeatures['src_eval_cnt']=default_val
        wfeatures['src_escape_cnt']=default_val
        wfeatures['src_link_cnt']=default_val
        wfeatures['src_underescape_cnt']=default_val
        wfeatures['src_exec_cnt']=default_val
        wfeatures['src_search_cnt']=default_val
        wfeatures['src_total_jfun_cnt']=default_val    
    
    return wfeatures

def safebrowsing(url):
    api_key = "ABQIAAAA8C6Tfr7tocAe04vXo5uYqRTEYoRzLFR0-nQ3fRl5qJUqcubbrw"
    name = "URL_check"
    ver = "1.0"

    req = {}
    req["client"] = name
    req["apikey"] = api_key
    req["appver"] = ver
    req["pver"] = "3.0"
    req["url"] = url #change to check type of url

    try:
        params = urllib.urlencode(req)
        req_url = "https://sb-ssl.google.com/safebrowsing/api/lookup?"+params
        res = urllib2.urlopen(req_url)
        # print res.code
        # print res.read()
        if res.code==204:
            # print "safe"
            return 0
        elif res.code==200:
            # print "The queried URL is either phishing, malware or both, see the response body for the specific type."
            return 1
        elif res.code==204:
            print "The requested URL is legitimate, no response body returned."
        elif res.code==400:
            print "Bad Request The HTTP request was not correctly formed."
        elif res.code==401:
            print "Not Authorized The apikey is not authorized"
        else:
            print "Service Unavailable The server cannot handle the request. Besides the normal server failures, it could also indicate that the client has been throttled by sending too many requests"
    except:
        return -1

def NumNumericChars(url):
    count=0
    for i in range(0,len(url)):
        if url[i].isdigit():
            count =count+1
    return count

def RandomString(url):
    urlstr = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+] |[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', url)	
    if (len(urlstr[0])==len(url)) and (len(urlstr)==1) :
        return 0
    return 1

def Statistical_report(url, ip_address):
    url_match = re.search(
        r'at\.ua|usa\.cc|baltazarpresentes\.com\.br|pe\.hu|esy\.es|hol\.es|sweddy\.com|myjino\.ru|96\.lt|ow\.ly', url)
    ip_match = re.search(
        '146\.112\.61\.108|213\.174\.157\.151|121\.50\.168\.88|192\.185\.217\.116|78\.46\.211\.158|181\.174\.165\.13|46\.242\.145\.103|121\.50\.168\.40|83\.125\.22\.219|46\.242\.145\.98|'
        '107\.151\.148\.44|107\.151\.148\.107|64\.70\.19\.203|199\.184\.144\.27|107\.151\.148\.108|107\.151\.148\.109|119\.28\.52\.61|54\.83\.43\.69|52\.69\.166\.231|216\.58\.192\.225|'
        '118\.184\.25\.86|67\.208\.74\.71|23\.253\.126\.58|104\.239\.157\.210|175\.126\.123\.219|141\.8\.224\.221|10\.10\.10\.10|43\.229\.108\.32|103\.232\.215\.140|69\.172\.201\.153|'
        '216\.218\.185\.162|54\.225\.104\.146|103\.243\.24\.98|199\.59\.243\.120|31\.170\.160\.61|213\.19\.128\.77|62\.113\.226\.131|208\.100\.26\.234|195\.16\.127\.102|195\.16\.127\.157|'
        '34\.196\.13\.28|103\.224\.212\.222|172\.217\.4\.225|54\.72\.9\.51|192\.64\.147\.141|198\.200\.56\.183|23\.253\.164\.103|52\.48\.191\.26|52\.214\.197\.72|87\.98\.255\.18|209\.99\.17\.27|'
        '216\.38\.62\.18|104\.130\.124\.96|47\.89\.58\.141|78\.46\.211\.158|54\.86\.225\.156|54\.82\.156\.19|37\.157\.192\.102|204\.11\.56\.48|110\.34\.231\.42',
        ip_address)
    if url_match:
        return 0
    elif ip_match:
        return 0
    else:
        return 1


def PctExtHyperlinks(url, soup, domain):
    i = 0
    unsafe = 0
    for a in soup.find_all('a', href=True):
        if "#" in a['href'] or "javascript" in a['href'].lower() or "mailto" in a['href'].lower() or not (url in a['href'] or domain in a['href']):
            unsafe = unsafe + 1
        i = i + 1
        # print a['href']
    try:
        percentage = unsafe / float(i) * 100
    except:
        return 1
    return percentage

def PctExtResourceUrls(url, soup, domain):
    i = 0
    success = 0
    for img in soup.find_all('img', src=True):
        dots = [x.start() for x in re.finditer(r'\.', img['src'])]
        if url in img['src'] or domain in img['src'] or len(dots) == 1:
            success = success + 1
        i = i + 1

    for audio in soup.find_all('audio', src=True):
        dots = [x.start() for x in re.finditer(r'\.', audio['src'])]
        if url in audio['src'] or domain in audio['src'] or len(dots) == 1:
            success = success + 1
        i = i + 1

    for embed in soup.find_all('embed', src=True):
        dots = [x.start() for x in re.finditer(r'\.', embed['src'])]
        if url in embed['src'] or domain in embed['src'] or len(dots) == 1:
            success = success + 1
        i = i + 1

    for i_frame in soup.find_all('i_frame', src=True):
        dots = [x.start() for x in re.finditer(r'\.', i_frame['src'])]
        if url in i_frame['src'] or domain in i_frame['src'] or len(dots) == 1:
            success = success + 1
        i = i + 1

    try:
        percentage = success / float(i) * 100
    except:
        return 1

    return percentage

def ExtFavicon(url, soup, domain):
    for head in soup.find_all('head'):
        for head.link in soup.find_all('link', href=True):
            dots = [x.start() for x in re.finditer(r'\.', head.link['href'])]
            return 1 if url in head.link['href'] or len(dots) == 1 or domain in head.link['href'] else -1
    return 1

def InsecureForms(url, soup, domain):
    for form in soup.find_all('form', action= True):
	if 'https' in form['action'] or '//' not in form['action']:
	      pass
	else:
	      return 0
    return 1

def AbnormalExtFormActionR(url, soup, domain):
    for form in soup.find_all('form', action= True):
           if 'https' in form['action'] or '//' not in form['action']:
              return -1
           elif url not in form['action'] and domain not in form['action']:
               return 0
           else:
               return 1

def MissingTitle(soup):
    for title in soup.find_all('title'):
           if title.text =='':
               	return 1
           else:
		return 0

def ImagesOnlyInForm(soup):
	for form in soup.find_all('form'):
		if form.find_all('img')!=None and form.text=='':
			return 1
		else:
			return 0

def SubdomainLevelRT(subdomain):
	if subdomain =='':
		return -1
	elif subdomain.count('.')==0:
		return 0
	else:
		return 1
def FrequentDomainNameMismatch(domain,soup):
     if soup =='':
	return 1
     for link in soup.find_all('link', href=True):
	if domain in link['href'] :
		return 0
     return 1
	

def FakeLinkInStatusBar(soup):
    if soup == "" :
        return 0
    else:
        if re.findall("<script>.+onmouseover.+</script>", soup.text):
            return 1
        else:
            return 0

def RightClickDisabled(soup):
    if soup == "":
        return -1
    else:
        if re.findall(r"event.button ?== ?2", soup.text):
            return 1
        else:
            return -1


def PopUpWindow(soup):
    if soup == "":
        return -1
    else:
        if re.findall(r"alert\(", soup.text):
            return 1
        else:
            return -1

def IframeOrFrame(soup):
    if soup == "":
        return -1
    else:
        if re.findall(r"[<iframe>|<frame>]", soup.text):
            return 1
        else:
            return -1

def SubmitInfoToEmail(soup):
    if soup == "":
        return -1
    else:
        if re.findall(r"[mail\(\)|mailto:?]", soup.text):
            return 1
        else:
            return -1

def RelativeFormAction(soup):
    for form in soup.find_all('form', action= True):
	if '//' not in form['action']  :
	     pass
	else:
	      return 0
    return 1

def AbnormalFormAction(soup):
    if soup =='':
	return 0
    for form in soup.find_all('form', action= True):
           if 'javascript:true' in form['action'] or form['action']=='' or '#' in form['action'] or 'about:blank' in form['action'] :
              return 1
           else:
              return 0

def AbnormalExtFormActionR(soup):
    if soup =='':
	return -1
    Abnormal=0
    total=0
    for form in soup.find_all('form', action= True):
           if 'javascript:true' in form['action'] or form['action']=='' or '#' in form['action'] or 'about:blank' in form['action'] :
              Abnormal+=1
           total+=1
    try:
    	percentage= Abnormal/total *100
    except:
	return 1
    if percentage < 22:
	return 1
    elif 22<= percentage<=61:
	return 0
    else:
	return -1

def ExtMetaScriptLinkRT(url, soup, domain):
    i = 0
    success = 0
    for link in soup.find_all('link', href=True):
        dots = [x.start() for x in re.finditer(r'\.', link['href'])]
        if url in link['href'] or domain in link['href'] or len(dots) == 1:
            success = success + 1
        i = i + 1

    for script in soup.find_all('script', src=True):
        dots = [x.start() for x in re.finditer(r'\.', script['src'])]
        if url in script['src'] or domain in script['src'] or len(dots) == 1:
            success = success + 1
        i = i + 1
    try:
        percentage = success / float(i) * 100
    except:
        return 1

    if percentage < 17.0:
        return 1
    elif 17.0 <= percentage < 81.0:
        return 0
    else:
        return -1


def UrlLengthRT(url):
    if len(url) < 75:
        return 1
    if 54 <= len(url) <= 75:
        return 0
    return -1

def PctExtResourceUrlsRT(url, soup, domain):
    i = 0
    success = 0
    for img in soup.find_all('img', src=True):
        dots = [x.start() for x in re.finditer(r'\.', img['src'])]
        if url in img['src'] or domain in img['src'] or len(dots) == 1:
            success = success + 1
        i = i + 1

    for audio in soup.find_all('audio', src=True):
        dots = [x.start() for x in re.finditer(r'\.', audio['src'])]
        if url in audio['src'] or domain in audio['src'] or len(dots) == 1:
            success = success + 1
        i = i + 1

    for embed in soup.find_all('embed', src=True):
        dots = [x.start() for x in re.finditer(r'\.', embed['src'])]
        if url in embed['src'] or domain in embed['src'] or len(dots) == 1:
            success = success + 1
        i = i + 1

    for i_frame in soup.find_all('i_frame', src=True):
        dots = [x.start() for x in re.finditer(r'\.', i_frame['src'])]
        if url in i_frame['src'] or domain in i_frame['src'] or len(dots) == 1:
            success = success + 1
        i = i + 1

    try:
        percentage = success / float(i) * 100
    except:
        return 1

    if percentage < 22.0:
        return 1
    elif 22.0 <= percentage < 61.0:
        return 0
    else:
        return -1
def PctExtNullSelfRedirectHyperlinksRT(soup):
    count=0
    total=0
    for link in soup.find_all('link', href=True):
	if link['href']=='' or link['href']=='#':
		count+=1
	total+=1
    
    try:
        percentage = count / float(total) * 100
    except:
        return 1

    if percentage < 22.0:
        return 1
    elif 22.0 <= percentage < 61.0:
        return 0
    else:
        return -1


def feature_extract(url_input,malicious):
        Feature={}
        tokens_words=re.split('\W+',url_input)       #Extract bag of words stings delimited by (.,/,?,,=,-,_)
        #print okens_words,len(tokens_words)
	print tokens_words
        #token_delimit1=re.split('[./?=-_]',url_input)
        #print token_delimit1,len(token_delimit1)
	r= requests.get(url_input)
	soup=BeautifulSoup(r.content,"lxml")
		
        obj=urlparse(url_input)
        host=obj.netloc
        path=obj.path
	query=obj.query
	print host
	subdomain,domain,suffix=tldextract.extract(url_input)
	print suffix
	Feature['subdomain']=len(subdomain.split('.'))
	Feature['PathLevel']=path.count('/')
        #Feature['URL']=url_input
        Feature['rank_host'],Feature['rank_country'] =rank(host)
	Feature['NumDash']=url_input.count('-')
	Feature['NumDashInHost']=host.count('-')
	Feature['AtSymbol']=re.match('@',url_input)
	Feature['TildeSymbol']=re.match('~',url_input)
	Feature['NumUnderscore']=url_input.count('_')
	Feature['NumPercent']=url_input.count('%')
	Feature['NumQueryComponents']=query.count('=')
	Feature['NumPercent']=url_input.count('%')
	Feature['NumAmpersand']=url_input.count('&')
	Feature['NumHash']=url_input.count('#')
	Feature['NumNumericChars']=NumNumericChars(url_input)
	Feature['NoHttps']=not(re.search('https', url_input))
	Feature['RandomString']=RandomString(url_input)
	Feature['IpAddress'],IP = Check_IPaddress(host)
	print IP
	Feature['DomainInSubdomains']= (suffix in subdomain)
	Feature['DomainInPaths']= (suffix in path)
	Feature['HttpsInHostname']= (re.search('http|https', host))
	Feature['HostnameLength']=len(host)
	Feature['DomainInPaths']= (domain in path)
	Feature['PathLength']= len(path)
	Feature['QueryLength']= len(query)
	Feature['DoubleSlashInPath']=('//' in path) 
	Feature['NumSensitiveWords']= Security_sensitive(tokens_words)
	Feature['Statistical_report']= Statistical_report(url_input,IP)
	Feature['PctExtHyperlinks']= PctExtHyperlinks(url_input, soup, domain)
	Feature['PctExtResourceUrls']=PctExtResourceUrls(url_input, soup, domain)
	Feature['RightClickDisabled']=RightClickDisabled(soup)
	Feature['PopUpWindow']=PopUpWindow(soup)
	Feature['IframeOrFrame']=IframeOrFrame(soup)
	Feature['SubmitInfoToEmail']=SubmitInfoToEmail(soup)
	Feature['ExtFavicon']=ExtFavicon(url_input, soup, domain)
        #Feature['path']=obj.path
        Feature['UrlLength']=len(url_input)
	Feature['PctExtNullSelfRedirectHyperlinksRT']=PctExtNullSelfRedirectHyperlinksRT(soup)
	Feature['MissingTitle']=MissingTitle(soup)
	Feature['ImagesOnlyInForm']=ImagesOnlyInForm(soup)
	Feature['SubdomainLevelRT']=SubdomainLevelRT(subdomain)
	Feature['UrlLengthRT']=UrlLengthRT(url_input)
	Feature['AbnormalExtFormActionR']=AbnormalExtFormActionR(soup)
        Feature['NumDots']=url_input.count('.')
	Feature['RelativeFormAction']=RelativeFormAction(soup)
	Feature['ExtMetaScriptLinkRT']=ExtMetaScriptLinkRT(url_input,soup,domain)
        Feature['AbnormalFormAction']=AbnormalFormAction(soup)
	Feature['PctExtResourceUrlsRT']=PctExtResourceUrlsRT(url_input,soup,domain) 			    	
        Feature['avg_domain_token_length'],Feature['domain_token_count'],Feature['largest_domain'] = Tokenise(host)
        Feature['avg_path_token'],Feature['path_token_count'],Feature['largest_path'] = Tokenise(path)
	Feature['avg_token_length'],Feature['token_count'],Feature['largest_token'] = Tokenise(url_input)
        Feature['URL']=url_input
	Feature['Malicious']=malicious
        
        # print host

        
        Feature['FakeLinkInStatusBar']=FakeLinkInStatusBar(soup)
	Feature['FrequentDomainNameMismatch']=FrequentDomainNameMismatch(domain,soup)
	Feature['PctNullSelfRedirectHyperlinks']=PctNullSelfRedirectHyperlinks(soup)
        """wfeatures=web_content_features(url_input)
        
        for key in wfeatures:
            Feature[key]=wfeatures[key]
        """
        #debug
        # for key in Feature:
        #     print key +':'+str(Feature[key])
        return Feature



url='https://www.24h.com.vn/'
print(feature_extract(url,0))

def main(url):
    filename='dataset.csv'
    dic=feature_extract(url)
    print dic
    df= pd.DataFrame([dic])
    print df
    df.to_csv(filename,index='false')






    
