#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import the necessary libraries

import tensorflow as tf
import numpy as np
import pandas as pd
from PIL import Image
from io import BytesIO
from flask import Flask, jsonify, request, render_template

import json
import pickle


# In[2]:


class Garbage_Collection_Point:
    garbage_type = ''
    collection_points = ['']


# In[3]:


class_labels = ['battery','brown-glass','cardboard','paper','plastic','shoes']

collection_points = {"collection point": ['Ecowrap',
                                          'Ecowrap',
                                          'Ecowrap',
                                          'RaddiDedo',
                                          'RaddiDedo',
                                          'Zero Waste Recycling Pvt Ltd',
                                          'Zero Waste Recycling Pvt Ltd',
                                          'Detoxen Enviro Solutions',
                                          'Detoxen Enviro Solutions',
                                          'Detoxen Enviro Solutions',
                                          'Detoxen Enviro Solutions',
                                          'Ecowrap',
                                          'Ecowrap',
                                          'Ecowrap'],
                     "garbage_type": ['battery','brown-glass','cardboard',
                                      'brown-glass','cardboard',
                                      'paper','plastic',
                                      'battery','brown-glass','cardboard','shoes',
                                      'brown-glass','cardboard', 'shoes'
                                     ],
                     }

garbage_collection_point_df = pd.DataFrame(collection_points)
#garbage_collection_point_df.sort_values(by='garbage_type')


# In[4]:


# testing code
# result = garbage_collection_point_df.loc[garbage_collection_point_df['garbage_type'] == 'battery', 'collection point'].tolist()
# #create object
# collection_points = Garbage_Collection_Point()
# collection_points.garbage_type = "battery"
# collection_points.collection_points = result

# predict_result = json.dumps(collection_points.__dict__)
    
# print (predict_result)


# In[5]:


# 1. define a prediction function

def predict_garbage(model, image_bytes):
    
    # Preprocess the image    
    image_bytes = image_bytes.resize((120, 120))
    image_bytes = np.array(image_bytes) / 255.0
    image_bytes = np.expand_dims(image_bytes, axis=0)
    
    # Make the prediction
    prediction = model.predict(image_bytes)
    predicted_class = class_labels[np.argmax(prediction)] 
    
    result = garbage_collection_point_df.loc[garbage_collection_point_df['garbage_type'] == predicted_class, 'collection point'].tolist()
    
    #create object
    collection_points = Garbage_Collection_Point()
    collection_points.garbage_type = predicted_class
    collection_points.collection_points = result
    
    predict_result = json.dumps(collection_points.__dict__)
    
    return predict_result


# In[6]:


# 2. create an instance of the flask class

app = Flask(__name__, template_folder='templates')


# In[7]:


# 3. load the model for predict

with open('models/garbage_classification_model_pickle.pkl', 'rb') as file:
    model = pickle.load(file)


# In[8]:


# 4. set up our home page

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])

# create a separate index.html page and then load it
def index():
    """Renders the home page, with a list of all polls."""
    
    return render_template('index.html', title='Home')


# In[9]:


# 5. define a new route to predict

@app.route('/predict', methods=['POST'])
def predict():
    
    # validation
    # Check if request contains a file
    if 'image' not in request.files:
        return jsonify({'error_message': "Request file is empty!"})
    
    # get the data from the request
    image_data = request.files['image'].read()
    image_bytes = Image.open(BytesIO(image_data))
    
    # make predictions on the data
    prediction_result = predict_garbage(model, image_bytes)   
    
    return prediction_result    


# In[10]:


# 6. allows the jupyter notebook to run flask using python app.py

if __name__ == '__main__':
    app.run()


# In[ ]:




