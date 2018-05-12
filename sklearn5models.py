import time

from scipy.signal import medfilt
from sklearn import tree, svm, neighbors
from sklearn.linear_model import SGDClassifier
from sklearn.naive_bayes import GaussianNB
from sklearnUtil import sklearn_modle, get_report_score

from preprocessData import load_dataset_from_h5

trainX, trainY, testX, testY, validX, validY = load_dataset_from_h5('data/datasetA.h5')

dtModel = tree.DecisionTreeClassifier()
svmModel = svm.SVC(decision_function_shape='ovo')
sgdModel = SGDClassifier(loss="hinge", penalty='l2')
knnModel = neighbors.KNeighborsClassifier(15, weights='distance')
gaussBayesModel = GaussianNB()

models_dict = {
    'decisionTree': dtModel,
    # 'SVM':svmModel,
    'sgd': sgdModel,
    # 'knn': knnModel,
    'gaussNB': gaussBayesModel,
    # 'randomForest':randomForest,
    # 'adaboost':adaboost,
    # 'mlp':mlp,
    # 'gradientBoost':gradientBoost,

}

res_dict = {}
for modleName, model in models_dict.items():
    start_time = time.time()
    clf = sklearn_modle(modleName, model, trainX, trainY)
    # predict_res = clf.predict(testX)
    # metrics = get_report_score(testY, predict_res, 'sing')
    predict_res = clf.predict(validX)
    metrics = get_report_score(validY, predict_res, 'sing')
    print('metrics:',metrics)
    stop_t = time.time() - start_time
    print('%s takes %i s' % (modleName, stop_t))
    res_dict[modleName] = [metrics, predict_res]
# sklearn_modle('decisionTree',dtModel,trainX,trainY)
print 'the res:', res_dict


# testPredictyY=dtModel.predict(testX)
# get_report_score(testY,testPredictyY,'sing')

# def do_the_vote(res_dict, testX, testY):
#     final_predict_after_vote = []
#     voteBox = []
#     # print type(res_dict)
#     for modelName, resValue in res_dict.items():
#         # print type(resValue[0][-1])
#         validWeight = int(resValue[0][-1] * 100)
#         clf = sklearn_modle(modelName, models_dict[modelName], testX, testY)
#         predict_res = clf.predict(testX)
#         # print('len pre res:',len(predict_res))
#         voteBox.append([validWeight, predict_res])
#     # print(voteBox)
#     for item in range(len(voteBox[0][1])):
#         frameRes = []
#         for modelItem in range(len(voteBox)):
#             frameRes.extend(voteBox[modelItem][0] * [voteBox[modelItem][1][item]])
#         if frameRes.count('sing') >= frameRes.count('nosing'):
#             final_predict_after_vote.append('sing')
#         else:
#             final_predict_after_vote.append('nosing')
#     return final_predict_after_vote
def do_the_vote(res_dict, testX, testY):
    final_predict_after_vote = []
    voteBox = []
    for modelName, resValue in res_dict.items():
        print(resValue)
        validWeight = int(resValue[0][-1] * 100)
        print(validWeight)
        clf = sklearn_modle(modleName, models_dict[modleName], testX, testY)
        predict_res = clf.predict(testX)
        voteBox.append([validWeight, predict_res])
    for item in range(len(voteBox[0][1])):
        frameRes = []
        for modelItem in range(len(voteBox)):
            frameRes.extend(voteBox[modelItem][0] * [voteBox[modelItem][1][item]])
        if frameRes.count('sing') >= frameRes.count('nosing'):
            final_predict_after_vote.append('sing')
        else:
            final_predict_after_vote.append('nosing')
    return final_predict_after_vote


# res = do_the_vote(res_dict, testX, testY)
print(res_dict)
res = do_the_vote(res_dict, testX, testY)

print('the report after vote')
get_report_score(testY, res, 'sing')

map_dict={'sing':1,'nosing':0}
map_res=[map_dict[lable] for lable in res]
# print(type(res))
filt_res=medfilt(map_res, 11)
print('the report after medfilt')
map_testY=[map_dict[lable] for lable in testY]
get_report_score(list(map_testY),list(filt_res),1)
