import os

import h5py
import librosa
import numpy
from librosa.feature import mfcc


def get_dataX_labelY(wav_dir='data/train'):
    dataX = []
    labelY = []
    all_files = os.listdir(wav_dir)
    for file_item in all_files:  # 1.get each wav file
        file_path = os.path.join(wav_dir, file_item)
        if '.wav' in file_path:
            audioData, sampleRate = librosa.load(file_path)
            wav_dir_name = wav_dir.split('/')[-1]
            lab_dir = wav_dir.replace(wav_dir_name, 'jamendo_lab')
            lab_name = file_item.replace('.wav', '.lab')
            lab_path = os.path.join(lab_dir, lab_name)  # 2.get lab file according to the wav file
            print(lab_path)
            with open(lab_path, 'r') as lab_txt:
                lab_cont = lab_txt.readlines()
                for lab_item in lab_cont:  # 3. get label info
                    lab_item_list = lab_item.split(' ')
                    start = int(float(lab_item_list[0]) * sampleRate)
                    end = int(float(lab_item_list[1]) * sampleRate)
                    label_info = lab_item_list[2][:-1]
                    segment = audioData[start:end]  # 4. extract segment mfcc
                    feat = mfcc(segment, sampleRate, n_mfcc=13)
                    dataX.append(feat)
                    labelY.extend([label_info] * feat.shape[1])  # 5.build label list Y
    dataX = numpy.concatenate(dataX, 1)  # 6. rebuild data array by combine all segment data features

    return dataX, labelY



if __name__ == '__main__':
    trainX, trainY = get_dataX_labelY('data/train')
    testX, testY = get_dataX_labelY('data/test')
    validX, validY = get_dataX_labelY('data/valid')
    dataset_file = h5py.File('data/datasetA.h5', 'w')  # 7. save the dataset to disk file
    dataset_file.create_dataset('trainX', data=trainX)
    dataset_file.create_dataset('trainY', data=trainY)
    dataset_file.create_dataset('testX', data=testX)
    dataset_file.create_dataset('testY', data=testY)
    dataset_file.create_dataset('validX', data=validX)
    dataset_file.create_dataset('validY', data=validY)
    dataset_file.close()
