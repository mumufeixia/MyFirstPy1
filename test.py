# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
# import os
# import tkinter as tk
# from tkinter import ttk
#
# win = tk.Tk()
# win.title("Python GUI")    # 添加标题
#
# ttk.Label(win, text="Chooes a number").grid(column=1, row=0)    # 添加一个标签，并将其列设置为1，行设置为0
# ttk.Label(win, text="Enter a name:").grid(column=0, row=0)      # 设置其在界面中出现的位置  column代表列   row 代表行
#
# # button被点击之后会被执行
# def clickMe():   # 当acction被点击时,该函数则生效
#   action.configure(text='Hello ' + name.get())     # 设置button显示的内容
#   action.configure(state='disabled')      # 将按钮设置为灰色状态，不可使用状态
#
# # 按钮
# action = ttk.Button(win, text="Click Me!", command=clickMe)     # 创建一个按钮, text：显示按钮上面显示的文字, command：当这个按钮被点击之后会调用command函数
# action.grid(column=2, row=1)    # 设置其在界面中出现的位置  column代表列   row 代表行
#
# # 文本框
# name = tk.StringVar()     # StringVar是Tk库内部定义的字符串变量类型，在这里用于管理部件上面的字符；不过一般用在按钮button上。改变StringVar，按钮上的文字也随之改变。
# nameEntered = ttk.Entry(win, width=12, textvariable=name)   # 创建一个文本框，定义长度为12个字符长度，并且将文本框中的内容绑定到上一句定义的name变量上，方便clickMe调用
# nameEntered.grid(column=0, row=1)       # 设置其在界面中出现的位置  column代表列   row 代表行
# nameEntered.focus()     # 当程序运行时,光标默认会出现在该文本框中
#
# # 创建一个下拉列表
# number = tk.StringVar()
# numberChosen = ttk.Combobox(win, width=12, textvariable=number)
# numberChosen['values'] = (1, 2, 4, 42, 100)     # 设置下拉列表的值
# numberChosen.grid(column=1, row=1)      # 设置其在界面中出现的位置  column代表列   row 代表行
# numberChosen.current(0)    # 设置下拉列表默认显示的值，0为 numberChosen['values'] 的下标值
#
# win.mainloop()      # 当调用mainloop()时,窗口才会显示出来

# import os
#
# os.system('ffmpeg')


# import os
# for root,dirs,files in os.walk('.'):
#     for file in files:
#         file_path = os.path.join(root,file)
#         # print file_path
#         if '.html' in file_path:
#             print file_path

# os.rename('./news.html','./news/news.html')





# print "Hello \nWorld"
#
#
# marker = '@@%&'
# names = ['a' , 'b' , 'C']
# for name in names:
#     print marker + name
#
# size = 40
# a = b = c = 3
# a,b,c=3,4,5
#
# print 'hello w' \
#       'orld'
# print  '''1321
# 342
# 43214
# 4312
# ret'''
#
# print len('hh')
#
# #list
# a = ['dgdg' , 'fg' ,100 ,1234 , 2*2]
# a[0] #'dgdg'
# a[:2]  # 'dgdg' , 'fg' ,
# a[2]=a[2]+23
#
# a , b = 0 ,1
# while(b < 1000):
#     print b,
#     a , b = b , a+b


# with open('cal.py','r') as cal:
#     cal_cont = cal.readline()
#     print cal_cont
#
#
# cal_file = open('cal.py','r')
# cal_cont = cal_file.readlines()
# print cal_cont[0]
# cal_file.close()

# cal_file = open('new.html','a')
# cal_cont = cal_file.writelines(['1\n','2,3\n'])
# cal_file.close()
from scipy.signal import medfilt
from sklearn import tree, svm, neighbors
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier

from preprocessData import load_dataset_from_h5
from sklearnUtil import sklearn_modle, get_report_score

trainX, trainY, testX, testY, validX, validY = load_dataset_from_h5('data/datasetA.h5')

dtModel = tree.DecisionTreeClassifier()
svmModel = svm.SVC(decision_function_shape='ovo')
sgdModel = SGDClassifier(loss="hinge", penalty="l2", n_iter=100)
knnModel = neighbors.KNeighborsClassifier(15, weights='distance')
gaussBayesModel = GaussianNB()
randomForest = RandomForestClassifier(n_estimators=10, max_depth=None, min_samples_split=2, random_state=0)
adaboost = AdaBoostClassifier(n_estimators=100)
gradientBoost = GradientBoostingClassifier(n_estimators=100, learning_rate=1.0,
                                           max_depth=1, random_state=0)
mlp = MLPClassifier(solver='lbfgs', alpha=1e-5,
                    hidden_layer_sizes=(5, 2), random_state=1)
models_dict = {
    # 'SVM': svmModel,
    # 'knn': knnModel,
    'randomForest': randomForest,
    'adaboost': adaboost,
    'mlp': mlp,
    'gradientBoost': gradientBoost,
    'decisionTree': dtModel,
    'sgd': sgdModel,
    'gaussNB': gaussBayesModel,
}

res_dict = {}
for modleName, model in models_dict.items():
    clf = sklearn_modle(modleName, model, trainX, trainY)
    predict_res = clf.predict(validX)
    metrics = get_report_score(validY, predict_res, 'sing')
    res_dict[modleName] = [metrics, predict_res]


def do_the_vote(res_dict, testX, testY):
    final_predict_after_vote = []
    voteBox = []
    for modelName, resValue in res_dict.items():
        validWeight = int(resValue[0][-1] * 100)
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


res = do_the_vote(res_dict, testX, testY)
print('the report after vote')
get_report_score(testY, res, 'sing')
map_dict = {'sing': 1, 'nosing': 0}
map_res = [map_dict[lable] for lable in res]
filt_res = medfilt(list(map_res), 11)
print('the report after filter')
map_testY = [map_dict[lable] for lable in testY]
get_report_score(list(map_testY), list(filt_res),1)