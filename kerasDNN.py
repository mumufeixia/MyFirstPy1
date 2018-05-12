from keras.callbacks import EarlyStopping
from keras.models import Sequential, load_model
from keras.layers import Dense,Dropout
from preprocessData import load_dataset_from_h5
from sklearnUtil import get_report_score

import  os

def map_lable_dict(res):
    map_dict = {'sing':1,'nosing':0}
    map_res = [map_dict[lable] for lable in res]
    return map_res

Retrain  = True
trainX, trainY, testX, testY, validX, validY = load_dataset_from_h5('data/datasetA.h5')
trainY=map_lable_dict(trainY)
testY=map_lable_dict(testY)
validY=map_lable_dict(validY)

if not os.path.isfile('model/dnn.model.h5') or Retrain:
    model = Sequential()

    model.add(Dense(units=13, activation='sigmoid', input_dim=13))
    model.add(Dropout(0.3))
    model.add(Dense(units=7, activation='relu'))
    # model.add(Dropout(0.2))
    # model.add(Dense(units=10,activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(units=1, activation='sigmoid'))

    model.compile(loss='binary_crossentropy',
                  optimizer='sgd',
                  metrics=['accuracy'])
    # ,'precision','recall','fmesaure'
    callbacks = [EarlyStopping(monitor='val_loss', patience=2, verbose=0)]

    model.fit(trainX,trainY,epochs=1,batch_size=32,callbacks=callbacks,validation_data=(validX,validY))
    model.save('model/dnn.model.h5')
    model.save_weights('model/dnn.weights.h5')
else:
    model=load_model('model/dnn.model.h5')
    model.load_weights('model/dnn.weights.h5')
# # model.train_on_batch()
# model.save('model/dnn.model.h5')
# model.save_weights('model/dnn.weights.h5')

loss_and_mertics = model.evaluate(validX,validY,batch_size=128)
print(loss_and_mertics)
# predictY = model.predict(testX,batch_size=128)
# res = get_report_score(testY,predictY,1)
# print('report_score:\n',res)




