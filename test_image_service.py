import json

import image_service

def test_jpg():
    event = {
        'body': json.dumps({
            'name': 'Urban Meyer',
            'id': 1,
            'image_url': 'https://image.cleveland.com/home/cleve-media/width600/img/osu_impact/photo/urban-meyer-2955543caf4124c2.jpg'
        })
    }
    lambda_response = image_service.lambda_handler(event, None)


def test_png():
    event = {
        'body': json.dumps({
            'name': 'PNG Pic',
            'id': 2,
            'image_url': 'https://upload.wikimedia.org/wikipedia/commons/4/47/PNG_transparency_demonstration_1.png'
        })
    }
    lambda_response = image_service.lambda_handler(event, None)


if __name__ == "__main__":
    print('\n\nTEST JPG\n')
    test_jpg()
    print('\n\nTEST PNG\n')
    test_png()
