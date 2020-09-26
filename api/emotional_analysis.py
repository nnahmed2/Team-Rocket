import os
import json
import flask
from tensorflow.keras import models
from preprocess import Preprocess
import numpy as np
from db import database

app = flask.Flask(__name__)
class_names = ['joy', 'fear', 'anger', 'sadness', 'neutral']
DB_PATH = os.path.join(os.getcwd(), 'db', 'mood.db')


def saveEntry(text, response_dict):
    ''' Used for saving the data '''

    emotions = list(response_dict.values())   ## getting the current emotional state (anger)
    decimal_values = emotions[1].values()   ## getting just the values of the moods like (joy = '0.02')

    ## creating the format that can be inserted into the db
    data = [emotions[0]]
    data.extend(list(decimal_values))
    data.append(text)

    mydb = database(DB_PATH)    ## connect and insert
    response_dict['saved'] = mydb.insertData(data)

    return response_dict


def getEntries():

    mydb = database(DB_PATH)
    return mydb.getData()


def getSentiment(text):
    ''' Get the sentiment from the given text using the pre-trained model
        Accepts:
            text -> user input message
        Return:
            response_json -> a json object 
    '''
    sentence = pre.convert(text)

    ## predict model ##
    pred = model.predict(sentence)

    ## create a dictionary for the response ##
    response_dict = {
        'mood' : class_names[np.argmax(pred)],
        'emotions' : {emotion : str(np.round(pred[0][index], decimals=3)) for index, emotion in enumerate(class_names)}
    }
    
    response_dict = saveEntry(text, response_dict) ## save to the DB

    return json.dumps(response_dict)      ## convert to json


@app.route('/api/', methods=["POST"])
def api():
    json_data = flask.request.json
    journal = json_data["journal"]
    return getSentiment(journal)        ## infer using the model


@app.route('/text/<journal>')
def text(journal):
    return getSentiment(journal)        ## infer using the model


@app.route('/get/')
def pastData():
    return getEntries()        ## get past database entries


pre = Preprocess()      ## prepare the texts for inference before starting the server

model_path = os.path.join(os.getcwd(), "model.h5")
model = models.load_model(model_path)       ## load model ##

app.run()