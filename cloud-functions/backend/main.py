import os
from google.cloud import pubsub
from flask import Response

def upload(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/0.12/api/#flask.Flask.make_response>`.
    """
    request_json = request.get_json()
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
