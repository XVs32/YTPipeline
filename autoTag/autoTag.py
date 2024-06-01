import json

from essentia.standard import MonoLoader, TensorflowPredictMusiCNN, TensorflowPredictVGGish
import numpy as np
import matplotlib.pyplot as plt

class autoTagCore():
    
    audio = None
    metadata = None

    def __init__(self):
        with open('msd-musicnn-1.json', 'r') as json_file:
            self.metadata = json.load(json_file)
    
    def load_audio(self, file_name):
        audio_file = '../download/' + file_name
        self.audio = MonoLoader(sampleRate=16000, filename=audio_file)()
        
    def tag(self):
        activations = TensorflowPredictMusiCNN(graphFilename='msd-musicnn-1.pb')(self.audio)

        result = None

        for slice in activations:
            if result is None:
                result = slice
            else:
                result += slice

        #find the id of the highest activation
        id = np.argmax(result)

        print(self.metadata["classes"][id])
        return self.metadata["classes"][id]
        
