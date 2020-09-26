import os
import json
import flask
from tensorflow.keras import models
from preprocess import Preprocess
import numpy as np

app = flask.Flask(__name__)
class_names = ['joy', 'fear', 'anger', 'sadness', 'neutral']

def getSentiment(sentence):
    ''' Get the sentiment from the given sentence using the pre-trained model
        Accepts:
            sentence -> user input message
        Return:
            response_json -> a json object 
    '''
    sentence = pre.convert(sentence)

    ## load model ##
    model_path = os.path.join(os.getcwd(), "model.h5")
    model = models.load_model(model_path)

    ## predict model ##
    pred = model.predict(sentence)

    ## create a dictionary for the response ##
    response_dict = {
        'mood' : class_names[np.argmax(pred)],
        'emotions' : {emotion : str(np.round(pred[0][index], decimals=3)) for index, emotion in enumerate(class_names)}
    }

    return json.dumps(response_dict)      ## convert to json

@app.route('/api/', methods=["POST"])
def api():
    json_data = flask.request.json
    journal = json_data["journal"]
    return getSentiment(journal)        ## infer using the model

@app.route('/text/<journal>')
def text(journal):
    return getSentiment(journal)        ## infer using the model

pre = Preprocess()    ## prepare the texts for inference before starting the server
app.run()