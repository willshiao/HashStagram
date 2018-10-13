import os
import torch
import pickle
import io

from google.cloud import pubsub, storage

from flask import Flask, Response, request
from singleton_decorator import singleton

import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torchvision.models as models

from wideresnet import *

app = Flask(__name__)

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)

@app.route("/")
def root():
    return "server alive"

@app.route("/upload", methods = ["POST"])
def upload():
    """
        Takes in a photo and attempts to serve to the user hashtags.
    """
    request_json = request.get_json()

    if request_json and 'photo' in request_json:
        model = app.config['MODEL']
        tensor = torch.rand(1,3,224,224)
        result = model.forward(tensor)
        return Response({"forwarded successfully"}, status=200)
    else:
        return Response({"Missing photo argument"}, status=400)
