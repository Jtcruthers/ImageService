import json

import image_service

def test():
    event = {
        'body': json.dumps({
            'name': 'Urban Meyer',
            'id': 1,
            'image_url': 'https://image.cleveland.com/home/cleve-media/width600/img/osu_impact/photo/urban-meyer-2955543caf4124c2.jpg'
        })
    }
    lambda_response = image_service.lambda_handler(event, None)


if __name__ == "__main__":
    test()
