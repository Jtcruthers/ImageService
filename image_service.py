import boto3
import json
import re
import requests
from collections import namedtuple
from uuid import uuid4

from PIL import Image

THUMBNAIL_SIZE = (400, 400)
STANDARD_SIZE = (2000, 2000)
S3_BUCKET = 'drone-part-picker-jtcruthers'

ImageData = namedtuple('POSTData', ['name', 'image'])


def load_image(image_url):
    tmp_file_path = f'/tmp/{uuid4().hex}'
    r = requests.get(image_url)
    if r.status_code < 200 or r.status_code > 299:
        raise Exception(f"Couldn't load image url {image_url}")

    with open(tmp_file_path, 'wb') as file_:
        for chunk in r:
            file_.write(chunk)

    print(f'Stored image from {image_url} to {tmp_file_path}')
    return Image.open(tmp_file_path)


def parse_event(event):
    body = json.loads(event['body'])
    image = load_image(body['image_url'])
    return ImageData(
        name=body['name'],
        image=image
    )


def create_file_name(image_data, size):
    base_name = f'{image_data.name}_{size}.jpg'
    return re.sub(r'\s', '_', base_name)


def get_s3_client():
    return boto3.client('s3')


def upload_to_s3(file_name, file_path):
    s3_client = get_s3_client()
    extra_args = { 'ContentType': 'image/jpeg' }
    s3_client.upload_file(
        file_path,
        S3_BUCKET,
        file_name,
        extra_args
    )


def create_thumbnail(image_data):
    file_name = create_file_name(image_data, 'thumb')
    file_path = f'/tmp/{file_name}'
    image = image_data.image
    image.thumbnail(THUMBNAIL_SIZE)
    image.convert('RGB').save(file_path)
    print(f'SAVING THUMBNAIL {file_path}')
    upload_to_s3(file_name, file_path)
    print(f'UPLOADING THUMBNAIL')
    return file_name


def create_standard_view(image_data):
    file_name = create_file_name(image_data, 'standard')
    file_path = f'/tmp/{file_name}'
    image = image_data.image
    image.thumbnail(STANDARD_SIZE)
    image.convert('RGB').save(file_path)
    print(f'SAVING STANDARD VIEW {file_path}')
    upload_to_s3(file_name, file_path)
    print(f'UPLOADING STANDARD VIEW')
    return file_name


def lambda_handler(event, context):
    image_data = parse_event(event)
    standard_file_name = create_standard_view(image_data)
    create_thumbnail(image_data)
    return {
        'statusCode': 200,
        'body': standard_file_name
    }
