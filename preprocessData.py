import os
import h5py

from pydub import AudioSegment

data_dir = 'data'


def transform_by_pydub(filePath, format):
    print(filePath, 'processing...')
    output_path = filePath.replace('../', '')[:-3] + 'wav'
    sound = AudioSegment.from_file(filePath, format)
    sound = sound.set_channels(1)
    sound = sound.set_frame_rate(16000)
    output_path_dir = os.path.dirname(output_path)
    if not os.path.isdir(output_path_dir):
        os.makedirs(output_path_dir)
    sound.export(output_path, 'wav')
    return 0


def format_to_wav():
    for root, dirs, names in os.walk(data_dir):
        for name in names:
            filePath = os.path.join(root, name)
            if '.ogg' in filePath:
                transform_by_pydub(filePath, 'ogg')
            elif 'mp3' in filePath:
                transform_by_pydub(filePath, 'mp3')
            else:
                pass

    return 0


# def load_dataset_from_h5(h5_path):
#     # print(h5_path)
#     h5file = h5py.File(h5_path,'r')
#
#     trainX = h5file['trainX'][:]
#     trainY = h5file['trainY'][:]
#     testX = h5file['testX'][:]
#     testY = h5file['testY'][:]
#     validX = h5file['validX'][:]
#     validY = h5file['validY'][:]
#     h5file.close()
#     return trainX.T,trainY,testX.T,testY,validX.T,validY

def load_dataset_from_h5(h5_path):
    h5file = h5py.File(h5_path, 'r')
    trainX = h5file['trainX'][:]
    trainY = h5file['trainY'][:]
    testX = h5file['testX'][:]
    testY = h5file['testY'][:]
    validX = h5file['validX'][:]
    validY = h5file['validY'][:]
    h5file.close()
    return trainX.T, trainY, testX.T, testY, validX.T, validY


if __name__ == '__main__':
    format_to_wav()