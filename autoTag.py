import json

from essentia.standard import MonoLoader, TensorflowPredictMusiCNN, TensorflowPredictVGGish
import numpy as np
import matplotlib.pyplot as plt

with open('msd-musicnn-1.json', 'r') as json_file:
    metadata = json.load(json_file)

audio_file = '/media/marco/share_area/Git/YTPipeline/AllMyself.wav'
audio = MonoLoader(sampleRate=16000, filename=audio_file)()

activations = TensorflowPredictMusiCNN(graphFilename='msd-musicnn-1.pb')(audio)

result = None

for slice in activations:
    if result is None:
        result = slice
    else:
        result += slice
        
#find the id of the highest activation 
id = np.argmax(result)

print(id)
print(result)
print(metadata["classes"][id])