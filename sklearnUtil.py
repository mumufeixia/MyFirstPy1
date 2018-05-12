import os
import time
import joblib

from sklearn.metrics import accuracy_score,precision_score,f1_score,recall_score

def sklearn_modle(model_name,model,trainX,trainY):
    start_time=time.time()
    clf_path = 'model/'+model_name+'.model'
    if os.path.isfile(clf_path):
        model = joblib.load(clf_path)
    else:
        print('begin fit ...%s'%{model_name})
        clf = model.fit(trainX, trainY)
        joblib.dump(clf, clf_path)
        stop_t=time.time()-start_time
        print('stop fit ...%s:%i' % (model_name, stop_t))

    return  model

def get_report_score(groundTrue,predictRes,posLable):
    acc = accuracy_score(groundTrue,predictRes)
    pre = precision_score(groundTrue,predictRes, pos_label=posLable)
    rec = recall_score(groundTrue,predictRes, pos_label=posLable)
    f1 = f1_score(groundTrue,predictRes, pos_label=posLable)
    print('acc:%.2f,pre:%.2f,rec:%.2f,f1:%.2f' % (acc, pre, rec, f1))
    return  acc, pre, rec, f1
