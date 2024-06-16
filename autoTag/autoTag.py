import json

from essentia.standard import MonoLoader, TensorflowPredictEffnetDiscogs, TensorflowPredict2D
import numpy as np



class autoTagCore():
    
    audio = None
    metadata = None

    def __init__(self):
        with open('autoTag/genre_discogs400-discogs-effnet-1.json', 'r') as json_file:
            self.metadata = json.load(json_file)
    
    def load_audio(self, file_name):
        audio_file = './download/' + file_name
        self.audio = MonoLoader(sampleRate=16000, filename=audio_file, resampleQuality=4)()
        
    def tag(self):
        
        embeddings = TensorflowPredictEffnetDiscogs(graphFilename="autoTag/discogs-effnet-bs64-1.pb", output="PartitionedCall:1")(self.audio)

        model = TensorflowPredict2D(graphFilename="autoTag/genre_discogs400-discogs-effnet-1.pb", input="serving_default_model_Placeholder", output="PartitionedCall:0")
        predictions = model(embeddings)

        result = None
        
        for slice in predictions:
            if result is None:
                result = slice
            else:
                result += slice

        #find the id of the highest activation
        id = np.argmax(result)

        #print(self.metadata["classes"][id])
        return self.metadata["classes"][id]
        
