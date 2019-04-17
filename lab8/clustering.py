from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.cluster import KMeans
import os
import fnmatch
import pandas as pd

d=pd.read_csv('resume_dataset.csv')
d=d.drop('ID',axis=1)
arr=d.values
data=arr[:,1:]
print data
vectorizer= TfidfVectorizer(max_df=1.0,max_features=100,stop_words='english',use_idf=True)
X=vectorizer.fit_transform(data)
km=KMeans(n_clusters=25,init='k-means++',max_iter=100,n_init=1,verbose=1)
print "Clustering "+km
res=km.fit(X)
print "Labels" +km.lables_
print " Cluster centers "+km.cluster_centers_.squeeze()
