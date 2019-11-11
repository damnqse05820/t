#!/usr/bin/python
# -*- coding: utf-8 -*-
from pyspark.ml import Pipeline, PipelineModel
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.feature import IndexToString, StringIndexer, VectorIndexer, VectorAssembler
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.mllib.evaluation import MulticlassMetrics
from Furniture import *
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.types import *
from pyspark.sql.functions import *
from pyspark.conf import SparkConf
from pyspark import SparkContext
from datetime import datetime
import os
java8_location= '/usr/lib/jvm/java-8-openjdk-amd64' # Set your own
os.environ['JAVA_HOME'] = java8_location
import glob
from functools import reduce
from datetime import datetime
import sys
import json
import re
'''
filename="data/dataset.csv"
spark =SparkSession.builder.master("local[12]").appName("URLDetector").config("spark.driver.memory", "12g").getOrCreate()
#spark.conf.set("spark.debug.maxToStringFields", 10000)
#spark.conf.set('spark.executor.cores', '3')
#spark.conf.set('spark.cores.max', '3')
#spark.conf.set("spark.driver.memory",'8g')
#spark.conf.set('spark.driver.maxResultSize', '8g')
modelpath="model"



def trainModel(trainingData):
        """ Ham huan luyen du lieu
        Mac dinh training toan bo du lieu trong dataset splitratio 100% training, 0% testing
    
        # Chuyen toan bo nhan thanh so neu chua chuyen
        # trainingData.select("label").groupBy("label").count().show()
    	labelIndexer = StringIndexer(inputCol="label", outputCol= "indexedLabel").fit(trainingData)
        # Chuyen toan bo gia tri thuoc tinh thanh so neu chua chuyen
    	featureIndexer = VectorIndexer(inputCol="features", outputCol= "indexedFeatures", maxCategories=4).fit(trainingData)
        # Khai bao thuat toan RandomForest
    	rf = RandomForestClassifier(labelCol="indexedLabel", featuresCol= "indexedFeatures", numTrees=20,maxDepth=5, maxBins=32, seed=None,impurity="gini")
        # Chuyen nhan du doan duoc tu dang so ve dang ban dau,
    	labelConverter = IndexToString(inputCol="prediction", outputCol="predictedLabel", labels=labelIndexer.labels)
        # Hop nhat tat ca cac buoc thanh mot luong duy nhat pipeline
    	pipeline = Pipeline(stages=[labelIndexer, featureIndexer, rf, labelConverter])
        
        # Train model qua pipeline
    	model = pipeline.fit(trainingData)
        model.write().overwrite().save(os.path.join(modelpath, "detector"))
    	return model

def evaluate(model, trainingData, testingData):
        # Ham kiem thu model, in ra man hinh do do chinh xac va thoi gian tinh toan

        time_train = 0
        time_test = 0
            
        if (not model):
            # Train model
            print("Training...")
            start_train = datetime.now()
            model = trainModel(trainingData)
            time_train = datetime.now() - start_train
        #print ("Num nodes: ", model.stages[2].totalNumNodes, "\n", model.stages[2].toDebugString, file=open("modelDebug.txt","w"))
        # Make predictions
        print("Testing...")
        start_test = datetime.now()
	print testingData.printSchema()
        predictions = model.transform(testingData)
	print predictions.printSchema()
	#print predictions.printSchema()
        time_test = datetime.now() - start_test

        # Evaluation for flow
        print("{:*^100}".format(""))
        print("Training time: ", time_train)
        print("Testing time: ", time_test)
        
        featureImportances = {}
        fi = model.stages[2].featureImportances
        features = loadcols(dataset)
        index = 0
        for value in fi:
            featureImportances[features[index]] = value
            index = index + 1
	#print featureImportances
        fiSorted = sorted(featureImportances.items(), key=lambda x: x[1], reverse=True)
        print("{:*^100}".format(" Feature Importances "))
        f = open("features_importance.txt", "w")
        for feature in fiSorted:
            if feature[1] > 0.0000:
                print "{!s} : {:.2%}".format(feature[0].strip(), feature[1])
            f.write("{!s}\n".format(feature[0].strip()))
        f.close()
        
        print ("{:*^100}".format(" Evaluate for Flow "))
        
        print ("Total predictions:", predictions.count())
        predictions.select("prediction", "indexedLabel", "label").groupBy("label").count().show()
        #print predictions.printSchema()
        predictionAndLabels = predictions.select("prediction", "indexedLabel").rdd
	
        metrics = MulticlassMetrics(predictionAndLabels)

        print "Confusion Matrix:"
	print  metrics.confusionMatrix()
        for line in metrics.confusionMatrix().toArray():
            print (line)
        
        print ("TPR: {:.3%} \tFPR: {:.3%}".format(metrics.truePositiveRate(1.0), metrics.falsePositiveRate(1.0)))
        print ("TNR: {:.3%} \tFNR: {:.3%}".format(metrics.truePositiveRate(0.0), metrics.falsePositiveRate(0.0)))

        print ("Precision: {:.3%} \tRecall: {:.3%} \tAccuracy: {:.3%}".format(metrics.precision(1.0), metrics.recall(1.0), metrics.accuracy))
        
        print (metrics.accuracy)

        print ("{:*^100}".format(""))
        
        # self.evaluateIP(predictions)

def predictionURL(url):
	

	#df.show()
	data= loadData(df,1).repartition(300).cache()
	predictions = model.transform(predictingData)


dataset=loadData(filename,0)
#print type(dataset)
trainingData,testingData=dataset.randomSplit([0.7, 0.3])
trainingData=trainingData.repartition(300).cache()
testingData =testingData.repartition(300).cache()

model= trainModel(trainingData)

#evaluate(model, trainingData, testingData)
predictionURL("https://www.youtube.com/watch?v=9ZsF5a_hNDU")
'''

def loadcols(dataset):
    col=[]
    for x in dataset.columns:
	if x == 'URL' or x == 'Malicious' or x == 'features' or x == 'label'or x == 'Unnamed' or x == '_c0':
	    continue
	col.append(x)
    return col

class Detector:
    """ Lop phat hien ma doc
    datapath: Duong dan den folder luu file du lieu dung cho huan luyen model, mac dinh: ./dataset
    modelpath: Duong dan den folder luu file model da duoc huan luyen, mac dinh: ./model
    """
    # conf = SparkContext.conf.setAll([('spark.executor.memory', '12g'), ('spark.app.name', 'Spark Updated Conf'), ('spark.executor.cores', '4'), ('spark.cores.max', '4'), ('spark.driver.memory','12g')])
    spark = SparkSession.builder.master("local[12]").appName("MalwareDetector").config("spark.driver.memory", "12g").getOrCreate()
    # spark.conf.set("spark.executor.memory", '45g')
    # spark.conf.set('spark.executor.cores', '4')
    # spark.conf.set('spark.cores.max', '4')
    # spark.conf.set("spark.driver.memory",'45g')
    # spark.conf.set('spark.driver.maxResultSize', '45g')
    spark.sparkContext.setLogLevel("ERROR")
    sc = spark.sparkContext
    def __init__(self, datapath="data/dataset.csv", modelpath="model",mode=1):
        self.datapath = datapath
        if mode == 0:
            self.dataset = self.loadDataset(datapath)
            (self.trainingData, self.testingData) = self.dataset.randomSplit([0.8, 0.2])
            self.trainingData = self.trainingData.repartition(300).cache()
            self.testingData = self.testingData.repartition(300).cache()
            self.modelpath = modelpath
            modelfile = os.path.join(self.modelpath, "detector")
            if (os.path.exists(modelfile)):
                print("Load model from: ", self.modelpath)
                self.model = PipelineModel.load(modelfile)
            else:
                print("Train new model")
                self.model = self.trainModel(self.dataset)
                #pass
        else:
            self.predictingData = self.loadDataset(datapath)
            self.predictingData = self.predictingData.repartition(300).cache()
            self.modelpath = modelpath
            modelfile = os.path.join(self.modelpath, "detector")
            if (os.path.exists(modelfile)):
                print("Load model from: ", self.modelpath)
                self.model = PipelineModel.load(modelfile)
            else:
                print("Train new model")
                self.model = self.trainModel(self.dataset)
                #pass
            #self.predict()

    def loadDataset(self, datapath):
        data = []
        
        # Doc vao files tu folder luu du lieu dung cho huan luyen
        if ".csv" in datapath:
            dataset = self.spark.read.csv(datapath, header=True, inferSchema=True)
        '''else:
            for filename in glob.glob(os.path.join(datapath,"*.csv"), recursive=True):
                d = self.spark.read.csv(filename, header=True, inferSchema=True)	
                data.append(d)
            # Hop nhat du lieu tu cac files du lieu
        dataset = unionAll(data)'''
        #print("len(data):", dataset.count())
        # dataset.fillna(0)
        # Hop nhat cac cot thuoc tinh thanh mot cot dat ten la "features"
	cols =loadcols(dataset)
	#print cols[55]
        assembler = VectorAssembler(inputCols=cols, outputCol="features")
        dataset = assembler.transform(dataset.dropna())
	#print dataset["features"][55]
        #print("len(data)v2:", dataset.count())
        dataset = dataset.withColumn("label", dataset['Malicious'])
        #print("len(data)v3:", dataset.count())
        # dataset = dataset.where(dataset["label"] != "SUSPICIOUS").repartition(300).cache()
        #print("len(data)v4:", dataset.count())
        return dataset
        
    
    def trainModel(self, trainingData):
        """ Ham huan luyen du lieu
        Mac dinh training toan bo du lieu trong dataset splitratio 100% training, 0% testing
        """
        # Chuyen toan bo nhan thanh so neu chua chuyen
        # trainingData.select("label").groupBy("label").count().show()
        labelIndexer = StringIndexer(inputCol="label", outputCol="indexedLabel").fit(trainingData)
        # Chuyen toan bo gia tri thuoc tinh thanh so neu chua chuyen
        featureIndexer = VectorIndexer(inputCol="features", outputCol="indexedFeatures", maxCategories=4).fit(trainingData)
        # Khai bao thuat toan RandomForest
        rf = RandomForestClassifier(labelCol="indexedLabel", featuresCol= "indexedFeatures", numTrees=25,maxDepth=5, maxBins=32, seed=None,impurity="gini")
        # Chuyen nhan du doan duoc tu dang so ve dang ban dau,
        labelConverter = IndexToString(inputCol="prediction", outputCol="predictedLabel", labels=labelIndexer.labels)
        # Hop nhat tat ca cac buoc thanh mot luong duy nhat pipeline
        pipeline = Pipeline(stages=[labelIndexer, featureIndexer, rf, labelConverter])
        
        # Train model qua pipeline
        model = pipeline.fit(trainingData)
        model.write().overwrite().save(os.path.join(self.modelpath, "detector"))
        return model
    
    def evaluate(self, model=None, trainingData=None, testingData=None):
        """ Ham kiem thu model, in ra man hinh do do chinh xac va thoi gian tinh toan
        """
        time_train = 0
        time_test = 0
        
        if (not trainingData):
            trainingData = self.trainingData
        if (not testingData):
            testingData = self.testingData
            
        if (not model):
            # Train model
            print("Training...")
            start_train = datetime.now()
            model = self.trainModel(trainingData)
            time_train = datetime.now() - start_train
        
        #print("Num nodes: ", model.stages[2].totalNumNodes, "\n", model.stages[2].toDebugString, file=open("modelDebug.txt","w"))
        # Make predictions
        print("Testing...")
        start_test = datetime.now()
        predictions = model.transform(testingData)
        time_test = datetime.now() - start_test

        # Evaluation for flow
        print("{:*^100}".format(""))
        print("Training time: ", time_train)
        print("Testing time: ", time_test)
        
        featureImportances = {}
        fi = model.stages[2].featureImportances
        features = loadcols(self.dataset)
        index = 0
        for value in fi:
            featureImportances[features[index]] = value
            index = index + 1
        fiSorted = sorted(featureImportances.items(), key=lambda x: x[1], reverse=True)
        print("{:*^100}".format(" Feature Importances "))
        f = open("features_importance.txt", "w")
        for feature in fiSorted:
            if feature[1] > 0.000:
                print("{!s} : {:.4%}".format(feature[0].strip(), feature[1]))
           # f.write("{!s}\n".format(feature[0].strip()))
        f.close()
        
        print("{:*^100}".format(" Evaluate for Flow "))
        
        print("Total predictions:", predictions.count())
        predictions.select("prediction", "indexedLabel", "label").groupBy("label").count().show()
        
        predictionAndLabels = predictions.select("prediction", "indexedLabel").rdd
        metrics = MulticlassMetrics(predictionAndLabels)

        print("Confusion Matrix:")
        for line in metrics.confusionMatrix().toArray():
            print(line)
        
        print("TPR: {:.3%} \tFPR: {:.3%}".format(metrics.truePositiveRate(1.0), metrics.falsePositiveRate(1.0)))
        print("TNR: {:.3%} \tFNR: {:.3%}".format(metrics.truePositiveRate(0.0), metrics.falsePositiveRate(0.0)))

        print("Precision: {:.3%} \tRecall: {:.3%} \tAccuracy: {:.3%}".format(metrics.precision(1.0), metrics.recall(1.0), metrics.accuracy))
        
        print(metrics.accuracy)

        print("{:*^100}".format(""))
        
        # self.evaluateIP(predictions)


        
    # Khoi tao sparkSession de su dung Spark
    #spark = SparkSession.builder.appName("MalwareDetector").getOrCreate()
    
    def predict(self): 
	print self.predictingData.show()
        predictions = self.model.transform(self.predictingData)
        #print predictions.show()
        df= predictions.select('prediction').collect()
        return df[0].asDict()["prediction"]


#if __name__ == "__main__":
#    """ HUONG DAN SU DUNG CLASS DETECTOR   
#    """
    # Khoi tao lop Detector
    #if int(sys.argv[1])==1:
  #  feature=feature_extract(sys.argv[1],0)
 #   if feature==-1:
#	f=open("output.txt",w)
#	f.write("1")
#	f.close()
#    else:
#    	filename="data/predictions.csv"
#    for i in feature:
#	print len(feature[i]),i
    	#df= pd.DataFrame(feature)	
    	#df.to_csv(filename,index='false')
    	#detector = Detector(mode=int(sys.argv[1]),datapath=filename)
    #else:
	#detector = Detector(mode=int(sys.argv[1]),datapath=sys.argv[2])
    #detector = Detector(mode=0)
    	#detector=Detector(mode=0)#,datapath=filename)
    # Chay kiem thu
    	#detector.evaluate()
    	#detector.predict()

def detect(md,url):	
        if md==0 :
                detector = Detector(mode=md)
                detector.evaluate()
        elif md ==1 :
                hostname,path,query,fragment=spliturl(url)
                if not re.search('^http',hostname):
                        if scanport(hostname):
                            url ='https://'+url
                        else :
                            url ='http://'+url
                furniture=feature_extract(url,0)
                if furniture ==-1 :
                        print("url is die")
                        return -1
                else:
                        filename="data/predictions.csv"
                        df= pd.DataFrame(furniture)
                        df.to_csv(filename,index='false')
                        detector = Detector(mode=md,datapath=filename)
                        return detector.predict()
        else:
                print("you input wrong ")
                return -1

if __name__ == "__main__":
	md=int(sys.argv[1] )
        if len(sys.argv)==3:
                url =sys.argv[2]
        else:
                url =''
        d=detect(md,url)
        if d==0:
            print("clear url")

        elif d == 1:
             print("malicious url")
        else:
           pass



