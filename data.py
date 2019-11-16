#!/usr/bin/python
# -*- coding: utf-8 -*-
import pandas as pd
from Furniture import *
from collections import defaultdict
import re
import threading
#import multiprocessing as mp
import time

def readdata(filename):
	dataset={}	
	data = pd.read_csv(filename,usecols=['url', 'label'],dtype={"url": str,'label':int},true_values = ['bad'],false_values = ['good'])
	dataset['url']=data['url']
	dataset['malware']=data['label']
	return dataset


#print dataset
def datafurniture(dic,data,start,end,steps):    
    
    for i in range(start,end,steps):
        if not 'http' in data['url'].iloc[i][:7]:
		hostname,path,query,fragment=spliturl(data['url'].iloc[i])
		if scanport(hostname)==1:
			url ='https://'+data['url'].iloc [i]
		else:
			url ='http://'+data['url'].iloc [i]
		
	else:
		url =data['url'].iloc [i]
	#print url
	print threading.current_thread().name,i,url,data['malware'].iloc[i]
    	dicti=feature_extract(url,data['malware'].iloc[i])
	for key,value in dicti.items():
		#print value[0]
	     if key !="URL":
		dic[key].append(value[0])
	     else:
		dic[key].append(data['url'].iloc [i])
		#print len(dic[key])
	#print threading.current_thread().name,i,url 
	#print data['url'][20003]

def writedata(data,filename):
    df= pd.DataFrame(data)	
    df.to_csv(filename,index='false')
    print "write successful"




#print worker(data,0,1)
#thread1 =threading.Thread(name='worker1',target=worker,args=(dataset,0,len(dataset['url'])//8))
#thread2 =threading.Thread(name='worker2',target=worker,args=(dataset,len(dataset['url'])//8,len(dataset['url'])//4))
#thread3 =threading.Thread(name='worker3',target=worker,args=(dataset,len(dataset['url'])//4,3*len(dataset['url'])//8)) 
#thread4 =threading.Thread(name='worker4',target=worker,args=(dataset,3*len(dataset['url'])//8,len(dataset['url'])//2)) 
#thread5 =threading.Thread(name='worker5',target=worker,args=(dataset,len(dataset['url'])//2,5*len(dataset['url'])//8))
#thread6 =threading.Thread(name='worker6',target=worker,args=(dataset,5*len(dataset['url'])//8,3*len(dataset['url'])//4))
#thread7 =threading.Thread(name='worker7',target=worker,args=(dataset,3*len(dataset['url'])//4,7*len(dataset['url'])//8))
#thread8 =threading.Thread(name='worker8',target=worker,args=(dataset,7*len(dataset['url'])//8,len(dataset['url'])))

def thread(dataset,start,end,threads,dic):
    for i in range(100):
    	t = threading.Thread(target=datafurniture,args=(dic,dataset,i+start,end,100))
    	threads.append(t)
    	t.start()
    for j in threads:
	j.join()


def check_thread(threads):
	for i in range(100):
		if threads[i].is_alive():
			time.sleep(5)
			return True
	return False 
			


def main ():
    dataset =readdata("data/url_all/dataset2.csv")
    #dic = defaultdict(list)
    #filename='data/dataset.csv'
    length= len(dataset['url'])//10000
    for i in range(1):
	dic = defaultdict(list)
	threads=[]
        thread(dataset,0,len(dataset['url']),threads,dic)
    #while check_thread(threads):
	#print "."
	filename1='data/predictions.csv'
    	writedata(dic,filename1)

main()


#thread1.start()
#thread2.start()
#thread3.start()
#thread4.start()
#thread5.start()
#thread6.start()
#thread7.start()
#thread8.start()


