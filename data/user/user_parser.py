from flask_restful import reqparse

post_parser = reqparse.RequestParser()
post_parser.add_argument('username', required=True)
post_parser.add_argument('email', required=True)
post_parser.add_argument('password', required=True)

put_parser = reqparse.RequestParser()
put_parser.add_argument('username', required=True)
put_parser.add_argument('email', required=True)
put_parser.add_argument('password', required=True)