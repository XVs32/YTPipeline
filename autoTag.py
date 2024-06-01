import json

from essentia.standard import MonoLoader, TensorflowPredictMusiCNN, TensorflowPredictVGGish
import numpy as np
import matplotlib.pyplot as plt

with open('msd-musicnn-1.json', 'r') as json_file:
    metadata = json.load(json_file)

print(metadata.keys())

audio_file = '/media/marco/share_area/Git/YTPipeline/AllMyself.wav'
audio = MonoLoader(sampleRate=16000, filename=audio_file)()

activations = TensorflowPredictMusiCNN(graphFilename='msd-musicnn-1.pb')(audio)

ig, ax = plt.subplots(1, 1, figsize=(10, 10))
ax.matshow(activations.T, aspect='auto')

ax.set_yticks(range(len(metadata['classes'])))
ax.set_yticklabels(metadata['classes'])
ax.set_xlabel('patch number')
ax.xaxis.set_ticks_position('bottom')
plt.title('Tag activations')
plt.show()