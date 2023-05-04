from requests import post, delete

HEIGHT = 100
WIDTH = 100
URL = "127.0.0.1:5000"


def generate_week_map():
    for _ in range(HEIGHT * WIDTH):
        post(f'http://{URL}/api/week', json={}).json()
    return {'success': 'OK'}


def clear_week_map():
    for i in range(HEIGHT * WIDTH):
        delete(f'http://{URL}/api/week/{i}').json()
    return {'success': 'OK'}


def main():
    print(generate_week_map())
    # print(clear_week_map())


if __name__ == '__main__':
    main()