import re
import os
import pandas as pd
import pickle

from nltk.tokenize import word_tokenize
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

class Preprocess:
    ''' Converts the raw text in the format that is usable for the model '''

    def __init__(self):
      
        self.max_seq_len = 500      ## max sequence length of a sentence/paragraph

        texts = self.load_data()
        
        ## we keep the tokenized text ready before starting the server to make faster inference 
        self.tokenizer = Tokenizer()
        self.tokenizer.fit_on_texts(texts)
        
    def load_data(self):
        ''' Loads the train and test dataset and combine into one '''

        curr_dir = os.getcwd()
        pkl_file = os.path.join(curr_dir, 'text_dump.pkl')

        if os.path.isfile(pkl_file):   ## if the pickle file exits, we open and get our sentences
            with open(pkl_file, 'rb') as f:
                return pickle.load(f)

        ## the file containing the text is not present. We create one for future use
        
        data_path = os.path.join(curr_dir, "data.csv")    ## open the data
        data = pd.read_csv(data_path)

        texts = [' '.join(self.clean_text(text)) for text in data.Text]

        # Use dumps to convert the object to a serialized string
        with open(pkl_file, 'wb') as f:
            pickle.dump(texts, f)

        return texts

    def clean_text(self, data):
        ''' Remove any symbols that are not helpful '''
        
        data = re.sub(r"(#[\d\w\.]+)", '', data)
        data = re.sub(r"(@[\d\w\.]+)", '', data)
        
        # tekenization using nltk
        return word_tokenize(data)

    def convert(self, journal):
        ''' Tokenize the words so that the sentence can be used for prediction '''

        seq = self.tokenizer.texts_to_sequences([journal])
        return pad_sequences(seq, maxlen=self.max_seq_len)

pre = Preprocess()