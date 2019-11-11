from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics
from sklearn.svm import SVC
import sys
import sklearn
import numpy as np
def loadcols(dataset):
    col=[]
    for x in dataset.columns:
        if x == 'URL' or x == 'Malicious' or x == 'features' or x == 'label'or x == 'Unnamed' or x == 'c0_':
            continue
        col.append(x)
        return col

class machine_learning_model:
    def __init__(self,mode=0):
        self.datapath="data/dataset.csv"
        data=pd.read_csv(self.datapath,low_memory=False)
        data= data.dropna()
        data= data.reset_index(drop=True)
        print len(data['Malicious'])
        #print type(data)
        #print data['Malicious']
        split_test_size = 0.3
        #print type(data)
        #print loadcols(data)
        feature_col_names = loadcols(data)
        predicted_class_names = ['Malicious']
        X = data[feature_col_names].values  # predictor feature columns

        y = data[predicted_class_names].values  # predicted class (1=true, 0=false) column
        #print X,y
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=split_test_size, random_state=0)
        if mode ==0:
            self.machine_learning_KNN()
        else:
            self.machine_learning_SVN()



    def machine_learning_KNN(self):
        knn = KNeighborsClassifier(n_neighbors = 3)
        #self.X_train.isnull(np.array([np.nan, 0], dtype=np.float64))
        #self.y_train.isnull(np.array([np.nan, 0], dtype=np.float64))
        knn.fit(self.X_train, np.ravel(self.y_train))
        knn_predict_test = knn.predict(self.X_test)
        print("Testing Accuracy: {0:.4f}".format(metrics.accuracy_score(self.y_test, knn_predict_test)))
        print(knn_predict_test)
        print("Confusion Matrix")
        print("{0}".format(metrics.confusion_matrix(self.y_test, knn_predict_test)))
        print()
        print("Classification Report")
        print(metrics.classification_report(self.y_test, knn_predict_test))
        # Model Precision: what percentage of positive tuples are labeled as such?
        print("Precision:",metrics.precision_score(self.y_test, knn_predict_test))

        # Model Recall: what percentage of positive tuples are labelled as such?
        print("Recall:",metrics.recall_score(self.y_test, knn_predict_test))
        #self.Accuracy(self.y_test, knn_predict_test)
        #predict_test = knn.predict(test1)
        #if(predict_test[0]==1):
        #   print("This is malware")
        #else:
        #   print("file clean")
    def machine_learning_SVN(self):
        svn=SVC(kernel='linear', C = 1.0)
        print svn
        print len(self.X_train)
        svn.fit(self.X_train, np.ravel(self.y_train))
        #print "2"  
        svn_predict_test =svn.predict(self.X_test)
        print("Testing Accuracy: {0:.4f}".format(metrics.accuracy_score(self.y_test, svn_predict_test)))
        print(svn_predict_test)
        print("Confusion Matrix")
        print("{0}".format(metrics.confusion_matrix(self.y_test,svn_predict_test)))
        print ()
        print ("Classification Report")
        print (metrics.classification_report(self.y_test, svn_predict_test))
        print ("Precision:",metrics.precision_score(self.y_test,svn_predict_test))
        # Model Recall: what percentage of positive tuples are labelled as
        print ("Recall:",metrics.recall_score(self.y_test, svn_predict_test))

def main():
    md=int(sys.argv[1])
    machine_learning_model(md)
main()
