{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "4d2a13fb",
   "metadata": {},
   "outputs": [],
   "source": [
    "# import required libraries\n",
    "\n",
    "import numpy as np\n",
    "import pandas as pd\n",
    "from PIL import Image\n",
    "from flask import Flask, jsonify, request, render_template\n",
    "\n",
    "import pickle"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "id": "cf5bb3f4",
   "metadata": {},
   "outputs": [],
   "source": [
    "# 1. create an instance of the flask class\n",
    "\n",
    "app = Flask(__name__, template_folder='templates')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "id": "f1552f0c",
   "metadata": {},
   "outputs": [],
   "source": [
    "# 2. define a prediction function\n",
    "\n",
    "def predict_iris_plant(model, input_json):\n",
    "    \n",
    "    class_labels = ['Setosa', 'Versicolor', 'Virginica']\n",
    "    \n",
    "    # make predictions on the data\n",
    "    predictions = model.predict(input_json)\n",
    "    \n",
    "    pred_labels = [class_labels[index] for index in predictions]\n",
    "    \n",
    "    return pred_labels"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "id": "04e121c3",
   "metadata": {},
   "outputs": [],
   "source": [
    "# 3. load the model for predict\n",
    "\n",
    "with open('models/iris_model_pickle.pkl', 'rb') as file:\n",
    "    model = pickle.load(file)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "id": "4027f6c5",
   "metadata": {},
   "outputs": [],
   "source": [
    "# 4. set up our home page\n",
    "\n",
    "@app.route('/', methods=['GET'])\n",
    "@app.route('/index', methods=['GET'])\n",
    "\n",
    "# create a separate index.html page and then load it\n",
    "def index():\n",
    "    \"\"\"Renders the home page, with a list of all polls.\"\"\"\n",
    "    \n",
    "    return render_template('index.html', title='Home')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "id": "1cd0fb18",
   "metadata": {},
   "outputs": [],
   "source": [
    "# 5. define a new route to predict\n",
    "\n",
    "@app.route('/predict', methods=['POST'])\n",
    "def predict():\n",
    "    \n",
    "    # get the data from the request\n",
    "    input_json = request.json\n",
    "    \n",
    "    # make predictions on the data\n",
    "    pred_labels = predict_iris_plant(model, input_json)   \n",
    "   \n",
    "    # return the predictions as a JSON response\n",
    "    return jsonify({'predictions': pred_labels})"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "613d7f3e",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      " * Serving Flask app \"__main__\" (lazy loading)\n",
      " * Environment: production\n",
      "\u001b[31m   WARNING: This is a development server. Do not use it in a production deployment.\u001b[0m\n",
      "\u001b[2m   Use a production WSGI server instead.\u001b[0m\n",
      " * Debug mode: off\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      " * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)\n",
      "127.0.0.1 - - [25/Mar/2023 13:42:07] \"GET / HTTP/1.1\" 200 -\n",
      "127.0.0.1 - - [25/Mar/2023 13:42:08] \"GET /favicon.ico HTTP/1.1\" 404 -\n",
      "127.0.0.1 - - [25/Mar/2023 13:42:41] \"POST /predict HTTP/1.1\" 200 -\n"
     ]
    }
   ],
   "source": [
    "# 6. allows the jupyter notebook to run flask using python app.py\n",
    "\n",
    "if __name__ == '__main__':\n",
    "    app.run()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 43,
   "id": "254a0b43",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "3.9.12 (main, Apr  4 2022, 05:22:27) [MSC v.1916 64 bit (AMD64)]\n"
     ]
    }
   ],
   "source": [
    "import sys\n",
    "print(sys.version)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "3b10c406",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.9.12"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
