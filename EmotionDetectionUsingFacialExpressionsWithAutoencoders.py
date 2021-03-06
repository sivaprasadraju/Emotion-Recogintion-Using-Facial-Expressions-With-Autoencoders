#-------------------------------------------------------------------------------
# Name:        EmotionDetectionUsingFacialExpressionsWithAutoencoders
# Purpose:
#
# Author:      sivaprasadrb
#
# Created:     10/11/2018
# Copyright:   (c) sivaprasadrb 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from __future__ import print_function
import keras
import os
from keras.layers import Input,Conv2D, MaxPooling2D, UpSampling2D,  Dense
from keras.models import Model
from keras.optimizers import RMSprop
from keras.preprocessing.image import ImageDataGenerator
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from keras import optimizers

import numpy as np
import matplotlib.pyplot as plt

data_path = './data/'

imgs = np.empty((256, 256), int)

filenames = sorted(os.listdir(data_path))
classificationLabels = []
count = 0
for img_name in filenames:
    img = plt.imread(data_path + img_name)
    img  = np.resize(img, (256, 256))
    if count == 0:
	imgs=(img)
	count = 1
    else:
    	imgs = np.append(imgs, img, axis=0)
    classificationLabels.append(int(img_name[1]))

imgs = np.reshape(imgs, [213, 256, 256])
print(imgs.shape)

train_images, test_images, train_labels, test_labels = train_test_split(imgs, d, test_size=0.33, random_state=42)

from keras.utils import to_categorical


print('Training data shape : ', train_images.shape, len(train_labels))

print('Testing data shape : ', test_images.shape, len(test_labels))

classes = np.unique(train_labels)

classes=np.append(classes,0)
nClasses = len(classes)

print('Total number of outputs : ', nClasses)
print('Output classes : ', classes)

plt.figure(figsize=[4,2])

plt.subplot(121)
plt.imshow(train_images[0,:,:], cmap='gray')
plt.title("Ground Truth : {}".format(train_labels[0]))

plt.subplot(122)
plt.imshow(test_images[0,:,:], cmap='gray')
plt.title("Ground Truth : {}".format(test_labels[0]))

print(train_images.shape[1:])
nRows,nCols = train_images.shape[1:]
nDims = nRows
print(nCols)
train_data = train_images.reshape(train_images.shape[0], nRows, nCols, 1)
test_data = test_images.reshape(test_images.shape[0], nRows, nCols, 1)
input_shape = (nRows, nCols, 1)

train_data = train_data.astype('float32')
test_data = test_data.astype('float32')

train_data /= 255
test_data /= 255

print(len(train_labels))
print(len(test_labels))

train_labels_one_hot = to_categorical(train_labels)
test_labels_one_hot = to_categorical(test_labels)

print(type(train_labels_one_hot))
print(type(train_labels))

print('Original label 0 : ', train_labels[0])
print('After conversion to categorical ( one-hot ) : ', train_labels_one_hot[0])

batch_size = 40
epochs = 50
inChannel = 1
x, y = 256,256
input_img = Input(shape = [x,y,inChannel])
print(input_img)

def autoencoder(input_img):
	encoded = Dense(128, activation='relu')(input_img)
	encoded = Dense(64, activation='relu')(encoded)
	encoded = Dense(32, activation='relu')(encoded)

	decoded = Dense(64, activation='relu')(encoded)
	decoded = Dense(128, activation='relu')(decoded)
	decoded= Dense(1, activation='relu')(decoded)
	print(type(encoded))
	print(type(decoded))
	return decoded

autoencoder = Model(input_img, autoencoder(input_img))
autoencoder.compile(loss='mean_squared_error', optimizer = RMSprop())

autoencoder.summary()
print(train_data.shape)
autoencoder_train = autoencoder.fit(train_data, train_data, batch_size=batch_size,epochs=epochs,verbose=1,validation_data=(test_data, test_data))

autoencoder.evaluate(test_data, test_labels_one_hot)