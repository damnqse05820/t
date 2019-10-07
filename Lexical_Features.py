import re
from bs4 import BeautifulSoup
import requests

def NumDots(url):
    return url.count('.')

def SubdomainLevel(subdomain):
    if subdomain =='':
	return 0
    else:
	return subdomain.count('.') +1

def PathLevel(path):
    return path.count('/')

def UrlLength(url):
    return len(url)

def NumDash(url):
    return url.count("-")

def NumDashInHostname(hostname):
    return hostname.count("-")

def AtSymbol(url):
    return 1 if url.count("@") else 0

def TildeSymbol(url):
    return 1 if url.count("~") else 0

def NumUnderscore(url):
    return url.count("_")

def NumPercent(url):
    return url.count("%")

def NumQueryComponents(query):
    return query.count("=")

def NumAmpersand(url):
    return url.count("&")

def NumHash(url):
    return url.count("#")

def NumNumericChars(url):
    x = re.findall("\d", url)
    return len(x)

def NoHttps(url):
    return 1 if "https" in url else 1

def IpAddress(hostname):
    IP=""
    try:
	IP=socket.gethostbyname(hostname)
	return 1,IP
    except:
	return 0,IP

def RandomString(url):	
    if ' ' in url :
        return 1
    return 0

#Checks if TLD or ccTLD is used as part of the subdomain in webpage URL
def DomainInSubdomains(subdomain,suffix):
    lists=suffix.split('.')
    for i in lists:
	if i in subdomain:
	   return 1
    return 0

#Checks if TLD or ccTLD is used as part of the path in webpage URL
def DomainInPath(path,suffix):
    lists=suffix.split('.')
    for i in lists:
	if i in path:
	   return 1
    return 0

def HttpsInHostname(hostname):
    return 1 if "https" in hostname or "http" in hostname else 0 

def HostnameLength(hostname):
    return len(hostname)

def PathLength(path):
    return len(path)

def QueryLength(query):
    return len(query)

def DoubleSlashInPath(path):
    return 1 if '//' in path else 0

def NumSensitiveWords(tokens_words):
    SensitiveWords=['confirm','account','banking','secure','ebayisapi','webscr','login','signin','blog','logon','signon',
'login.asp', 'login.php', 'login.htm', '.exe', '.zip', '.rar', '.jpg','.gif', 'viewer.php', 'link=', 'getImage.asp', 'plugins','paypal',
'order', 'dbsys.php', 'config.bin', 'download.php', 'payment', 'files', 'css', 'shopping', 'mail.php', '.jar', '.swf', '.cgi',
'.php', 'abuse', 'admin', '.bin', 'personal', 'update', 'verification']
    count=0
    for ele in SensitiveWords:
        if(ele in tokens_words):
            count+=1;
    return count


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


