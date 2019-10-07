import re

def SubdomainLevelRT(subdomain):
	if subdomain =='':
		return -1
	elif subdomain.count('.')==0:
		return 0
	else:
		return 1

def UrlLengthRT(url):
    if len(url) < 75:
        return 1
    if 54 <= len(url) <= 75:
        return 0
    return -1

def PctExtResourceUrlsRT(url, soup, domain):
    if soup =='':
	return -1
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
    if soup =='':
	return -1
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

def PctExtNullSelfRedirectHyperlinksRT(soup):
    if soup =='':
	return -1
    count=0
    total=0
    for link in soup.find_all('link', href=True):
	if link['href']=='' or link['href']=='#':
		count+=1
	total +=1
    
    try:
        percentage = count / float(total) * 100
    except:
        return 1

    return percentage
