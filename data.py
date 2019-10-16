import pandas as pd
from Furniture import *
from collections import defaultdict
import re
import threading
import socket
import time
def readdata(filename):
	dataset={}	
	data = pd.read_csv(filename,usecols=['url', 'label'],dtype={"url": str,'label':int})
	dataset['url']=data['url']
	dataset['malware']=data['label']
	return dataset


#print dataset
def datafurniture(dic,data,start,end,steps):    
    
    for i in range(start,end,steps):
	if not '://' in data['url'][i]:
		url =search_in_google(data['url'][i])
	else:
		url =data['url'][i]
	#print url
    	dicti=(feature_extract(url,data['malware'][i]))    
	for key,value in dicti.items():
		dic[key].append(value)
	dic["URL"].append(data['url'][i])
	print threading.current_thread().name,i
	#print data['url'][20003]

def writedata(data,filename):
    df= pd.DataFrame(data)	
    df.to_csv(filename,index='false')




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
    for i in range(10):
    	t = threading.Thread(target=datafurniture,args=(dic,dataset,i+start,end,10))
    	threads.append(t)
    	t.start()


def check_thread(threads):
	for i in range(10):
		if threads[i].is_alive():
			time.sleep(5)
			return True
	return False 
			


def main ():
    dataset =readdata("data/url_all/dataset1.csv")
    threads=[]
    dic = defaultdict(list)
    filename='data/dataset.csv'
    thread(dataset,20000,80000,threads,dic)
    while check_thread(threads):
	print "."
    writedata(dic,filename)

#main()


#thread1.start()
#thread2.start()
#thread3.start()
#thread4.start()
#thread5.start()
#thread6.start()
#thread7.start()
#thread8.start()


