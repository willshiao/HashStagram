import os
import torch
import pickle
import io
import numpy
from PIL import Image
import logging

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

@app.route("/api/upload", methods = ["POST"])
def upload():
    """
        Takes in a photo and attempts to serve to the user hashtags.
    """
    request_json = request.get_json()

    if request.files and 'photo' in request.files:
        photo = request.files['photo']
        img = Image.open(photo)
        app.logger.error(img)
        width, height = img.size
        app.logger.error(str(width) + " " +  str(height))
        data = numpy.asarray(img, dtype=numpy.float32)
        app.logger.error(data)
        #data = numpy.reshape(data, (3, width, height))
        tensor = torch.from_numpy(data).unsqueeze_(0)
        app.logger.error(tensor)
        model = app.config['MODEL']
        app.logger.error(model)
        #return Response({str(tensor.size())}, status=200)
        #tensor = torch.rand(1,3,224,224)
        result = model.forward(tensor)
        return Response({"forwarded successfully"}, status=200)
    else:           
        return Response({"Missing photo argument"}, status=400)
