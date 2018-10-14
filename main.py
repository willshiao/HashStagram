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

def convert_to_hashtag(results):
    hashtag_list = []
    for i in torch.topk(results, 5)[-1]:
        hashtag_list.append(app.config['TAG_MAP'][i])
    return hashtag_list

@app.route("/api/upload", methods = ["POST"])
def upload():
    """
        Takes in a photo and attempts to serve to the user hashtags.
    """
    request_json = request.get_json()

    if request.files and 'photo' in request.files:
        photo = request.files['photo']
        img = Image.open(photo)
        img = img.resize((224,224))
        app.logger.error(img)

        width, height = img.size
        app.logger.error(str(width) + " " +  str(height))
        
        data = numpy.asarray(img, dtype=numpy.float32)
        data = numpy.reshape(data, (3, width, height))
        app.logger.error(data.shape)

        tensor = torch.from_numpy(data).unsqueeze_(0)
        app.logger.error(tensor.size())
        
        model = app.config['MODEL']
        #return Response({str(tensor.size())}, status=200)
        #tensor = torch.rand(1,3,224,224)
        result = model.forward(tensor)
        result = convert_to_hashtag(result)
        return Response({str(result)}, status=200)
    else:           
        return Response({"Missing photo argument"}, status=400)
