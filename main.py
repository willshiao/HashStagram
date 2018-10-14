import os
import torch
import pickle
import io
import numpy
from PIL import Image
import logging

from google.cloud import pubsub, storage

from flask import Flask, Response, request, render_template, json
from flask_cors import CORS
from singleton_decorator import singleton

import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torchvision.models as models
from torchvision import transforms

from wideresnet import *

app = Flask(__name__)
CORS(app)
normalize = transforms.Normalize(
    mean=[0.485, 0.456, 0.406],
    std=[0.229, 0.224, 0.225]
)

preprocess = transforms.Compose([
    transforms.Resize(224),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    normalize
])
def convert_to_hashtag(row):
    app.logger.error(row)
    return [app.config['TAG_MAP'][x] for x in row]

@app.route("/api/upload", methods = ["POST"])
def upload():
    """
        Takes in a photo and attempts to serve to the user hashtags.
    """
    request_json = request.get_json()

    if request.files and 'photo' in request.files:
        photo = request.files['photo']
        print(type(photo))
        img = Image.open(io.BytesIO(photo.read()))
        app.logger.error("img type" + str(type(img)))
        tensor = preprocess(img)
        if (tensor.size()[0] > 3):
            tensor = torch.from_numpy(tensor.numpy()[0:3, :, :])
        tensor = torch.unsqueeze(tensor, 0)


        
        app.logger.error(tensor.size())
        
        model = app.config['MODEL']
        #return Response({str(tensor.size())}, status=200)
        #tensor = torch.rand(1,3,224,224)
        result = model.forward(tensor)
        app.logger.error(result.size())
        result = convert_to_hashtag(torch.topk(result[0], 5)[1].numpy())
        return json.jsonify(data=result, status = "success")
    else:           
        return Response({"Missing photo argument"}, status=400)
