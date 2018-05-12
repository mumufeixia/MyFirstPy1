# from sklearn import tree
# from sklearn.datasets import load_iris
import os
import time
import joblib
from sklearn import tree
from preprocessData import load_dataset_from_h5
from sklearn.metrics import accuracy_score,precision_score,f1_score,recall_score

start_time=time.time()

trainX,trainY,testX,testY,validX,validY =load_dataset_from_h5('data/datasetA.h5')
clf = tree.DecisionTreeClassifier()
print(type(trainX),trainX.shape)

clf_path='dt.modle'
if os.path.isfile(clf_path):
    clf=joblib.load(clf_path)
else:
    clf = clf.fit(trainX,trainY)
    joblib.dump(clf,clf_path)

print(clf.predict(testX))

# iris = load_iris()
#
# print(iris.data, iris.target)
# print(len(iris.data))

# clf = tree.DecisionTreeClassifier()
# clf = clf.fit(iris.data, iris.target)
# print (clf.predict(iris.data))
def getErr(pre, tru):
    err = 0
    for pr, tr in zip(pre, tru):
        if pr != tr:
            err += 1
    return err / 1.0 / len(pre)

# print(getErr(clf.predict(iris.data), iris.target))

# print(getErr(clf.predict(testX), testY))
# print(getErr(clf.predict(trainX), trainY))
# print(getErr(clf.predict(validX), validX))

testPredictyY=clf.predict(testX)
acc = accuracy_score(testY,testPredictyY)
pre = precision_score(testY,testPredictyY,pos_label='sing')
rec = recall_score(testY,testPredictyY,pos_label='sing')
f1 = f1_score(testY,testPredictyY,pos_label='sing')
print(getErr(clf.predict(testX), testY))
end_time= time.time()
dur_time=end_time-start_time

print('acc:%.2f,pre:%.2f,rec:%.2f,f1:%.2f\nit takes %i s'%(acc,pre,rec,f1,dur_time))