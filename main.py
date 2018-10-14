import os
import torch
import pickle
import io
import numpy
from PIL import Image

from google.cloud import pubsub, storage

from flask import Flask, Response, request, render_template
from flask_cors import CORS
from singleton_decorator import singleton

import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torchvision.models as models

from wideresnet import *

app = Flask(__name__)
CORS(app)

@app.route('/', methods = ["GET"])
def index():
    return render_template('index.html')

@app.route("/upload", methods = ["POST"])
def upload():
    """
        Takes in a photo and attempts to serve to the user hashtags.
    """
    request_json = request.get_json()

    if request.files and 'photo' in request.files:
        photo = request.files['photo']
        img = Image.open(photo)
        width, height = img.size
        data = numpy.asarray(img, dtype=numpy.float32)
        data = numpy.reshape(data, (3, width, height))
        tensor = torch.from_numpy(data).unsqueeze(0)
        model = app.config['MODEL']
        #return Response({str(tensor.size())}, status=200)
        #tensor = torch.rand(1,3,224,224)
        result = model.forward(tensor)
        return Response({"forwarded successfully"}, status=200)
    else:
        return Response({"Missing photo argument"}, status=400)
