import boto3
import json
import re
from collections import namedtuple

from flask import Flask, request
from PIL import Image

app = Flask(__name__)

THUMBNAIL_SIZE = (150, 150)
STANDARD_SIZE = (2000, 2000)

ImageData = namedtuple('ImageData', ['name', 'alt', 'id', 'image'])

def parse_event(event):
    body = event['body']
    image = Image.open(body['image'])
    return ImageData(
        body['name'],
        body['alt'],
        body['id'],
        image
    )


def create_file_name(image_data, size):
    base_name = f'{image_data.name}_{image_data.alt}_{image_data.id}_{size}.jpg'
    return re.sub(r'\s', '_', base_name)


def create_thumbnail(image_data):
    file_name = create_file_name(image_data, 'thumb')
    image = image_data.image
    image.thumbnail(THUMBNAIL_SIZE)
    image.save(f'/Users/justin.carruthers/Desktop/{file_name}')


def create_standard_view(image_data):
    file_name = create_file_name(image_data, 'standard')
    image = image_data.image
    image.thumbnail(STANDARD_SIZE)
    image.save(f'/Users/justin.carruthers/Desktop/{file_name}')
    return file_name


def lambda_handler(event, context):
    image_data = parse_event(event)
    standard_file_name = create_standard_view(image_data)
    create_thumbnail(image_data)
    return {
        'statusCode': 200,
        'body': standard_file_name
    }


@app.route('/')
def test():
    request_image = request.files['image']
    event = {
        'body': {
            'name': request.form['name'],
            'alt': request.form['alt'],
            'id': request.form['id'],
            'image': request.files['image']
        }
    }
    lambda_response = lambda_handler(event, None)
    return f'Passed to lambda handler successfully {lambda_response["body"]}'

