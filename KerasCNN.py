from __future__ import print_function

from time import time

import keras
import numpy
from keras.callbacks import EarlyStopping
from keras.datasets import cifar10
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential, load_model
from keras.layers import Dense, Dropout, Activation, Flatten, Conv1D, MaxPooling1D
from keras.layers import Conv2D, MaxPooling2D
import os
from preprocessData import load_dataset_from_h5

def map_lable_dict(res):
    map_dict = {'sing':1,'nosing':0}
    map_res = [map_dict[lable] for lable in res]
    return map_res

num_classes = 2

Retrain  = True
time_step = 29
model_saved_path = 'model/cnn.model.h5'
model_weights_saved_path = model_saved_path.replace('.model', '.weights')
def get_step_data(dataX,dataY,step=time_step):
    finalX =[]
    finalY=[]
    lenTX=len(dataX[0])
    for i_y in range(0,len(dataY),step):
        if list(dataY[i_y:i_y+step]).count(1)==step:
            finalY.append(1)
            finalX.append(dataX[i_y:i_y+step])
        if list(dataY[i_y:i_y+step]).count(0)==step:
            finalY.append(0)
            finalX.append(dataX[i_y:i_y+step])

    finalX=numpy.array(finalX)
    finalY=numpy.array(finalY)
    finalX=numpy.reshape(finalX,(-1,step,lenTX))

    return finalX,finalY

def build_load_model(trainX,trainY,testX,testY, validX, validY ):
    if not os.path.isfile('model/cnn.model.h5') or Retrain:
        model = Sequential()
        feat_dim = numpy.shape(trainX)[-1]
        VERBOSE =1
        # print(trainX)ValueError: Input 0 is incompatible with layer conv2d_1: expected ndim=4, found ndim=2
        # print('type Of trainX',type(trainX))
        # print(trainX.shape[1:])
        # print('type Of trainX', type(trainX.shape[1:]))
        # print('type Of trainX', type(trainX.shape[1]))
        # model.add(Conv1D((4,4),input_shape=(time_step,feat_dim),activation='relu')))#,padding='same',input_shape=trainX.shape[1:]
        model.add(Conv1D(4, 4, input_shape=(time_step, feat_dim), activation='relu'))
        # model.add(Activation('relu'))
        # model.add(Conv2D(32,(3,3)))
        # model.add(Activation('relu'))
        # model.add(MaxPooling2D(pool_size=(2,2)))
        # model.add(Dropout(0.25))

        # model.add(Conv2D(64,(3,3),padding='same'))
        # model.add(Activation('relu'))
        # model.add(Conv2D(64,(3,3)))
        # model.add(Activation('relu'))
        # model.add(MaxPooling2D(pool_size=(2,2)))
        # model.add(Dropout(0.25))

        # model.add(Flatten())
        # model.add(Dense(512))
        # model.add(Activation('relu'))
        # # model.add(Dropout(0.5))
        # model.add(Dense(num_classes))
        # model.add(Activation('softmax'))
        #
        #
        # opt = keras.optimizers.rmsprop(lr=0.0001,decay=1e-6)
        #
        #
        # model.compile(loss='binary_crossentropy',
        #               optimizer='sgd',
        #               metrics=['accuracy'])
        # ,'precision','recall','fmesaure'
        model.add(MaxPooling1D(2))
        model.add(Conv1D(4, 4, activation='relu'))
        model.add(MaxPooling1D(2))
        model.add(Flatten())
        model.add(Dense(1, activation='sigmoid'))
        model.compile(loss='binary_crossentropy',
                      optimizer='adam',
                      metrics=['accuracy'])

        print(model.summary())

        callbacks = [EarlyStopping(monitor='val_loss', patience=2, verbose=0)]

        # trainX = trainX.astype('float32')
        # testX = testX.astype('float32')
        # trainX /= 255
        # testX /= 255

        model.fit(trainX,trainY,batch_size=128,nb_epoch=10000, callbacks=callbacks, validation_data=(validX, validY),
                  verbose=VERBOSE)
        model.save('model/cnn.model.h5')
        model.save_weights('model/cnn.weights.h5')
    elif Retrain != True and os.path.isfile(model_saved_path) and os.path.isfile(model_weights_saved_path):
        model= load_model('model/cnn.model.h5')
        model.load_weights('model/cnn.weights.h5')
        model.compile(loss='binary_crossentropy',
                      optimizer='adam',
                      metrics=['accuracy'])
    else:
        model = 'null'
        print('error')

    loss_and_metrics = model.evaluate(testX, testY, batch_size=128, verbose=0)
    predictY = model.predict_classes(testX)
    print(loss_and_metrics)
    return 0



if __name__ == '__main__':
    start_time = time()
    trainX, trainY, testX, testY, validX, validY = load_dataset_from_h5('data/datasetA.h5')
    trainY = map_lable_dict(trainY)
    testY = map_lable_dict(testY)
    validY = map_lable_dict(validY)

    trainX, trainY=get_step_data(trainX, trainY)
    testX, testY = get_step_data(testX, testY)
    validX, validY = get_step_data(validX, validY)
    # trainY = keras.utils.to_categorical(trainY, num_classes)
    # testY = keras.utils.to_categorical(testY, num_classes)
    # validY = keras.utils.to_categorical(validY, num_classes)
    build_load_model(trainX, trainY, testX, testY, validX, validY)
    end_time=time()
    print('it takes %.1f s' %(end_time-start_time))
    # scores = model.evaluate(testX, testY, verbose=1)
    # print('test loss:', scores[0])
    # print('test accuraqcy:', scores[1])


