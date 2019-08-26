import json
from flask import Flask, request
from PIL import Image


app = Flask(__name__)

THUMBNAIL_SIZE = (150, 150)
NORMAL_SIZE = (1920, 1080)


def lambda_handler(event, context):
    message = event['body']
    return {
        'statusCode': 200,
        'body': json.dumps(f'{event}')
    }


@app.route('/')
def test():
    request_image = request.files['image']
    image = Image.open(request_image)
    image.thumbnail((50, 50))
    image.save('/Users/justin.carruthers/Desktop/thumby.jpg')

    return 'Hello'

