import torch
import numpy as np
#import pandas as pd
import scipy.stats as si



SEQ_LENGTH=20
BOOTSTRAP_SIZE=10000
NUMBER_OF_BATCHS=4



def data_to_input(sequence, pos_or_neg):
    mapping = {'A': 0, 'R': 1, 'N': 2, 'D': 3, 'C': 4, 'E': 5, 'Q': 6, 'G': 7, 'H': 8, 'I': 9, 'L': 10, 'K': 11,
               'M': 12, 'F': 13, 'P': 14, 'S': 15, 'T': 16, 'W': 17, 'Y': 18, 'V': 19}
    map=np.zeros((9, 20))
    for i, seq in enumerate(sequence):
        map[i,mapping[seq]]+=1
    map = map.flatten()
    return np.concatenate([map, np.array([pos_or_neg])])


def Read_Data(filename, pos_or_neg):
    file = open(filename, 'r')
    lines=file.readlines()
    if pos_or_neg==1:
        DATA=np.zeros((len(lines), 181))
        for i, line in enumerate(lines):
            input = data_to_input(line.replace('\n', ''), pos_or_neg)
            DATA[i] = input
        DATA=bootstrap(DATA, BOOTSTRAP_SIZE, NUMBER_OF_BATCHS)
    else:
        DATA = np.zeros((len(lines), 181))
        for i, line in enumerate(lines):
            input = data_to_input(line.replace('\n', ''), pos_or_neg)
            DATA[i] = input
    return DATA


def bootstrap(DATA,size,NUMBER_OF_BATCHS):

    new_DATA=np.zeros((size,181))
    N=DATA.shape[0]
    batch_size=N//NUMBER_OF_BATCHS
    for i in range(NUMBER_OF_BATCHS):

        random = np.random.randint(batch_size*i,batch_size*(i+1), size=size//NUMBER_OF_BATCHS)
        new_DATA[((size//NUMBER_OF_BATCHS)*i):(size//NUMBER_OF_BATCHS)*(i+1), :] = DATA[random, :]
    return new_DATA

def DATA_pre_pros(filename_pos,filename_neg):

    neg_data=Read_Data(filename_neg, 0)
    pos_data=Read_Data(filename_pos, 1)
    final_data = np.concatenate([neg_data, pos_data])
    np.random.shuffle(final_data)
    train_set = final_data[:int(len(final_data)*0.9)]
    test_set = final_data[int(len(final_data)*0.9):]
    return train_set, test_set



def shuffle_data(data_Xy):
    np.random.shuffle(data_Xy)
    return data_Xy[:,:180],data_Xy[:,-1]
