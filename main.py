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

@singleton
class RES_HASHNET(nn.Module):
    def __init__(self):
        super(RES_HASHNET, self).__init__()
        self.object_extractor = models.resnet18(pretrained=True)
        self.object_extractor.eval()
        self.background_extractor = resnet18(pretrained=True)
        self.background_extractor.eval()
        self.fc1 = nn.Linear(2000,4096)
        self.fc2 = nn.Linear(4096,4096)
        self.output = nn.Linear(4096,1000)
    def forward(self, x):
        obj_feat = self.object_extractor(x)
        print(obj_feat.size())
        scene_feat = self.background_extractor(x)
        print(scene_feat.size())
        feats = torch.cat((obj_feat, scene_feat), dim=1)
        output = self.fc1(feats)
        output = self.fc2(output)
        output = self.output(output)
        return output

model = RES_HASHNET()

# initializes model by loading into memory from trained model
@app.before_first_request
def load_model():
    app.logger.info("loading")
    client = storage.Client()
    bucket = client.get_bucket("models_cta003")
    blob = bucket.get_blob("TEHBESTMODEL.pth")
    blob.download_to_filename("model.tsh")

    modeldict = torch.load("model.tsh")
    model.load_state_dict(modeldict)
    app.logger.info("finished initial loading")


@app.route("/upload", methods = ["POST"])
def upload():
    """
        Takes in a photo and attempts to serve to the user hashtags.
    """
    request_json = request.get_json()

    #if os.getenv('mechanism_type') == 'pubsub':
    #    if request_json and 'photo' in request_json:
    #        publisher = pubsub.PublisherClient()
    #        topic_name = 'projects/{project_id}/topics/{topic}'.format(
    #            project_id=os.getenv('GOOGLE_CLOUD_PROJECT'),
    #            topic=os.getenv('topic_name'),  # Set this to something appropriate.
    #        )
    #        publisher.publish(topic_name, b'Test', photo=request_json['photo'])
    #        return Response({topic_name + " published"}, status=200);
    #    else:
    #        return Response({"Missing photo argument"},status=400)

    #elif os.getenv('mechanism_type') == 'storage':
    if request_json and 'photo' in request_json:
        tensor = torch.rand(1,3,224,224)
        result = model.forward(tensor)
        return Response({"forwarded successfully"}, status=200)
    else:
        return Response({"Missing photo argument"}, status=400)
    #else:
    #    return Response({"Misconfiguration error, contact administrator"}, status=500)
