from pyspark.ml import Pipeline
from pyspark.ml.classification import DecisionTreeClassifier
from pyspark.ml.feature import StringIndexer, VectorIndexer
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
import pandas as pd
# Load training data

filename="data/dataset0.csv"
data  = pd.read_csv(filename)
for column in list(set(data.columns[0][5])):
	print data[column]

inCol=["NumDots","SubdomainLevel","PathLevel","NumDash","NumDashInHost","AtSymbol","TildeSymbol","NumUnderscore","NumPercent","NumQueryComponents","NumAmpersand","NumHash","NumNumericChars","NoHttps","RandomString","IpAddress","DomainInSubdomains","HttpsInHostname","HostnameLength","DomainInPaths","PathLength","QueryLength","DoubleSlashInPath","NumSensitiveWords","rank_host","rank_country","AgeDomain","Statistical_report","PctExtHyperlinks","PctExtResourceUrls","RightClickDisabled","PopUpWindow","IframeOrFrame","SubmitInfoToEmail","ExtFavicon","UrlLength","PctExtNullSelfRedirectHyperlinksRT","MissingTitle","ImagesOnlyInForm","SubdomainLevelRT","UrlLengthRT","AbnormalExtFormActionR","RelativeFormAction","ExtMetaScriptLinkRT","PctExtResourceUrlsRT","AbnormalFormAction","avg_domain_token_length","domain_token_count","largest_domain","avg_path_token","path_token_count","largest_path","avg_token_length","token_count","largest_token","FakeLinkInStatusBar","FrequentDomainNameMismatch","PctNullSelfRedirectHyperlinks","src_html_cnt","src_hlink_cnt","src_iframe_cnt","src_search_cnt","src_exec_cnt","src_underescape_cnt","src_link_cnt","src_escape_cnt","src_eval_cnt","src_total_jfun_cnt"]
outCol="Malicious"
#Decision tree classifier

# Load the data stored in LIBSVM format as a DataFrame.
#data = spark.read.format("libsvm").load("data/mllib/sample_libsvm_data.txt")

# Index labels, adding metadata to the label column.
# Fit on whole dataset to include all labels in index.
labelIndexer = StringIndexer(inputCol=inCol,outputCol=outCol).fit(data)
# Automatically identify categorical features, and index them.
# We specify maxCategories so features with > 4 distinct values are treated as continuous.
featureIndexer =VectorIndexer(inputCol="features", outputCol="indexedFeatures", maxCategories=4).fit(data)

# Split the data into training and test sets (30% held out for testing)
(trainingData, testData) = data.randomSplit([0.7, 0.3])

# Train a DecisionTree model.
dt = DecisionTreeClassifier(labelCol="indexedLabel", featuresCol="indexedFeatures")

# Chain indexers and tree in a Pipeline
pipeline = Pipeline(stages=[labelIndexer, featureIndexer, dt])

# Train model.  This also runs the indexers.
model = pipeline.fit(trainingData)

# Make predictions.
predictions = model.transform(testData)

# Select example rows to display.
predictions.select("prediction", "indexedLabel", "features").show(5)

# Select (prediction, true label) and compute test error
evaluator = MulticlassClassificationEvaluator(
    labelCol="indexedLabel", predictionCol="prediction", metricName="accuracy")
accuracy = evaluator.evaluate(predictions)
print ("Decision tree classifier")
print ("Test Error = %g " % (1.0 - accuracy))

treeModel = model.stages[2]
# summary only
print(treeModel)

#Random forest classifier

from pyspark.ml import Pipeline
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.feature import IndexToString, StringIndexer, VectorIndexer
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

# Load and parse the data file, converting it to a DataFrame.
#data = spark.read.format("libsvm").load("data/mllib/sample_libsvm_data.txt")

# Index labels, adding metadata to the label column.
# Fit on whole dataset to include all labels in index.
labelIndexer = StringIndexer(inputCol=inCol, outputCol=outCol).fit(data)
print labelIndexer
# Automatically identify categorical features, and index them.
# Set maxCategories so features with > 4 distinct values are treated as continuous.
featureIndexer = VectorIndexer(inputCol="features", outputCol="indexedFeatures", maxCategories=4).fit(data)

# Split the data into training and test sets (30% held out for testing)
(trainingData, testData) = data.randomSplit([0.7, 0.3])

# Train a RandomForest model.
rf = RandomForestClassifier(labelCol="indexedLabel", featuresCol="indexedFeatures", numTrees=10)

# Convert indexed labels back to original labels.
labelConverter = IndexToString(inputCol="prediction", outputCol="predictedLabel",labels=labelIndexer.labels)

# Chain indexers and forest in a Pipeline
pipeline = Pipeline(stages=[labelIndexer, featureIndexer, rf, labelConverter])

# Train model.  This also runs the indexers.
model = pipeline.fit(trainingData)
#important furniture
print model.featureImportances
# Make predictions.
predictions = model.transform(testData)

# Select example rows to display.
predictions.select("predictedLabel", "label", "features").show(5)

# Select (prediction, true label) and compute test error
evaluator = MulticlassClassificationEvaluator(
    labelCol="indexedLabel", predictionCol="prediction", metricName="accuracy")
accuracy = evaluator.evaluate(predictions)
print ("Random forest classifier")
print ("Test Error = %g" % (1.0 - accuracy))

rfModel = model.stages[2]
print (rfModel)  # summary only

#Gradient-boosted tree classifier

from pyspark.ml import Pipeline
from pyspark.ml.classification import GBTClassifier
from pyspark.ml.feature import StringIndexer, VectorIndexer
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

# Load and parse the data file, converting it to a DataFrame.
#data = spark.read.format("libsvm").load("data/mllib/sample_libsvm_data.txt")

# Index labels, adding metadata to the label column.
# Fit on whole dataset to include all labels in index.
labelIndexer =StringIndexer(inputCol=inpCol,outputCol=outCol).fit(data)
# Automatically identify categorical features, and index them.
# Set maxCategories so features with > 4 distinct values are treated as continuous.
featureIndexer =VectorIndexer(inputCol="features", outputCol="indexedFeatures", maxCategories=4).fit(data)

# Split the data into training and test sets (30% held out for testing)
(trainingData, testData) = data.randomSplit([0.7, 0.3])

# Train a GBT model.
gbt = GBTClassifier(labelCol="indexedLabel", featuresCol="indexedFeatures", maxIter=10)

# Chain indexers and GBT in a Pipeline
pipeline = Pipeline(stages=[labelIndexer, featureIndexer, gbt])

# Train model.  This also runs the indexers.
model = pipeline.fit(trainingData)

# Make predictions.
predictions = model.transform(testData)

# Select example rows to display.
predictions.select("prediction", "indexedLabel", "features").show(5)

# Select (prediction, true label) and compute test error
evaluator = MulticlassClassificationEvaluator(
    labelCol="indexedLabel", predictionCol="prediction", metricName="accuracy")
accuracy = evaluator.evaluate(predictions)
print "Gradient-boosted tree classifier"
print ("Test Error = %g" % (1.0 - accuracy))

gbtModel = model.stages[2]
print (gbtModel)  # summary only






