import os
from google.cloud import pubsub, storage
from flask import Response
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from wideresnet import *
import torch
import json

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

def upload(request):
    """
        Takes in a photo and attempts to serve to the user hashtags.
    """
    request_json = request.get_json()

    if os.getenv('mechanism_type') == 'pubsub':
        if request_json and 'photo' in request_json:
            publisher = pubsub.PublisherClient()
            topic_name = 'projects/{project_id}/topics/{topic}'.format(
                project_id=os.getenv('GOOGLE_CLOUD_PROJECT'),
                topic=os.getenv('topic_name'),  # Set this to something appropriate.
            )
            publisher.publish(topic_name, b'Test', photo=request_json['photo'])
            return Response({topic_name + " published"}, status=200);
        else:
            return Response({"Missing photo argument"},status=400)

    elif os.getenv('mechanism_type') == 'storage':
        if request_json and 'photo' in request_json:
            client = storage.Client()
            bucket = client.get_bucket(os.getenv('bucket_name'))
            blob = bucket.get_blob(os.getenv('trained_model_name'))
            pthmodel = blob.download_as_string()
            
            modeldict = json.loads(pthmodel)
            model = RES_HASHNET()
            model.load_state_dict(modeldict)
            tensor = torch.rand(1,3,224,224)
            model.forward(tensor)

            return Response({"Loaded successfully"}, status=200)
        else:
            return Response({"Missing photo argument"}, status=400)
    else:
        return Response({"Misconfiguration error, contact administrator"}, status=500)
