from requests import post, delete
from flask import jsonify

HEIGHT = 100
WIDTH = 100
URL = "127.0.0.1:5000"


def generate_month_map():
    for _ in range(HEIGHT * WIDTH):
        post(f'http://{URL}/api/month', json={}).json()
    return {'success': 'OK'}


def clear_month_map():
    for i in range(HEIGHT * WIDTH):
        delete(f'http://{URL}/api/month/{i}').json()
    return {'success': 'OK'}


def main():
    print(generate_month_map())
    # print(clear_month_map())


if __name__ == '__main__':
    main()