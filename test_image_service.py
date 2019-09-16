import json

import image_service

def test_jpg(monkeypatch):
    monkeypatch.setattr('test_image_service.image_service.upload_to_s3', lambda x, y: 1)
    event = {
        'body': json.dumps({
            'name': 'Urban Meyer',
            'id': 1,
            'image_url': 'https://image.cleveland.com/home/cleve-media/width600/img/osu_impact/photo/urban-meyer-2955543caf4124c2.jpg'
        })
    }
    lambda_response = image_service.lambda_handler(event, None)


def test_png(monkeypatch):
    monkeypatch.setattr('test_image_service.image_service.upload_to_s3', lambda x, y: 1)
    event = {
        'body': json.dumps({
            'name': 'PNG Pic',
            'id': 2,
            'image_url': 'https://upload.wikimedia.org/wikipedia/commons/4/47/PNG_transparency_demonstration_1.png'
        })
    }
    lambda_response = image_service.lambda_handler(event, None)
