from requests import post, delete
from flask import jsonify

HEIGHT = 100
WIDTH = 100
URL = "127.0.0.1:5000"


def generate_day_map():
    for _ in range(HEIGHT * WIDTH):
        post(f'http://{URL}/api/day', json={}).json()
    return {'success': 'OK'}


def clear_day_map():
    for i in range(HEIGHT * WIDTH):
        delete(f'http://{URL}/api/day/{i}').json()
    return {'success': 'OK'}


def main():
    print(generate_day_map())
    # print(clear_day_map())


if __name__ == '__main__':
    main()