import re
import urllib2
def PctExtHyperlinks(url, soup, domain):
    if soup=="":
	return 0
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
    if soup=="":
	return 0
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
    if soup=="":
	return 0
    for head in soup.find_all('head'):
        for head.link in soup.find_all('link', href=True):
            dots = [x.start() for x in re.finditer(r'\.', head.link['href'])]
            return 1 if url in head.link['href'] or len(dots) == 1 or domain in head.link['href'] else -1
    return 1

def InsecureForms(url, soup, domain):
    if soup=="":
	return 0
    for form in soup.find_all('form', action= True):
	if 'https' in form['action'] or '//' not in form['action']:
	      pass
	else:
	      return 0
    return 1

def RelativeFormAction(soup):
    if soup=="":
	return 0
    for form in soup.find_all('form', action= True):
	urlstr=re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', form['action'])
	if len(urlstr) >0:
	     return 1
	else:
	     return 0
    return 0

def PctNullSelfRedirectHyperlinks(soup):
    if soup=="":
	return 0
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

def AbnormalFormAction(soup):
    if soup =='':
	return 0
    for form in soup.find_all('form', action= True):
           if 'javascript:true' in form['action'] or form['action']=='' or '#' in form['action'] or 'about:blank' in form['action'] :
              return 1
           else:
              return 0
    return 0

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

def SubmitInfoToEmail(soup):
    if soup == "":
        return -1
    else:
        if re.findall(r"[mail\(\)|mailto:?]", soup.text):
            return 1
        else:
            return -1

def IframeOrFrame(soup):
    if soup == "":
        return -1
    else:
        if re.findall(r"[<iframe>|<frameBorder>]", soup.text):
            return 1
        else:
            return -1


def MissingTitle(soup):
    if soup == "":
        return 1
    for title in soup.find_all('title'):
          if title.text =='':
               	return 1
          else:
		return 0

def ImagesOnlyInForm(soup):
    	if soup == "":
        	return 0
	for form in soup.find_all('form'):
		if form.find_all('img')!=None and form.text=='':
			return 1
		else:
			return 0
	return 0



def web_content_features(url,soup):#search cac the 
    wfeatures={}
    total_cnt=0
    try:        

        #print source_code[:500]

        wfeatures['src_html_cnt']=soup.count('<html')
        wfeatures['src_hlink_cnt']=soup.count('<a href=')
        wfeatures['src_iframe_cnt']=soup.count('<iframe')
        #suspicioussrc_ javascript functions count

        wfeatures['src_eval_cnt']=soup.count('eval(')
        wfeatures['src_escape_cnt']=soup.count('escape(')
        wfeatures['src_link_cnt']=soup.count('link(')
        wfeatures['src_underescape_cnt']=soup.count('underescape(')
        wfeatures['src_exec_cnt']=soup.count('exec(')
        wfeatures['src_search_cnt']=soup.count('search(')
        
        for key in wfeatures:
            if(key!='src_html_cnt' and key!='src_hlink_cnt' and key!='src_iframe_cnt'):
                total_cnt+=wfeatures[key]
        wfeatures['src_total_jfun_cnt']=total_cnt
    
    except Exception, e:
        #print "Error"+str(e)+" in downloading page "+url 
        default_val=-1
        
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

