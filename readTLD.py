#!/usr/bin/python
#-*- coding: utf-8 -*-
from io import open
def readTLDs():
    filename="TLDs_of_domain.txt"
    tldlist=[]
    f=open(filename, encoding="ascii",mode="r",errors="ignore")
    utldlist=f.readlines()
    #print tldlist
    for i in utldlist:
	try :
        	tld=i.encode('ascii','ignore')
	except:
		continue
        if len(tld)>2:
                if not tld[:2]=="//" or tld[:1] ==" ":
                        tldlist.append(tld)

    return tldlist

def TLD():
        ls=[]
        for i in readTLDs():
                if not '.' in i:
                        ls.append(i)
        return ls

#print readTLDs()
