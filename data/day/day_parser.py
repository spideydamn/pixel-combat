from flask_restful import reqparse

put_parser = reqparse.RequestParser()
put_parser.add_argument('color', required=True)

post_parser = reqparse.RequestParser()
post_parser.add_argument('color', required=False)