from flask_restful import Resource, abort
from flask import jsonify

from .. import db_session
from .month import Month
from .month_parser import post_parser, put_parser


def abort_if_pixel_not_found(pixel_id):
    session = db_session.create_session()
    pixel = session.query(Month).get(pixel_id)
    if not pixel:
        abort(404, message=f"Pixel {pixel_id} not found")


class MonthResource(Resource):
    def get(self, pixel_id):
        abort_if_pixel_not_found(pixel_id)
        session = db_session.create_session()
        pixel = session.query(Month).get(pixel_id)
        return jsonify({'pixels': pixel.to_dict(
            only=("id", "color", "painter_id"))})

    def delete(self, pixel_id):
        abort_if_pixel_not_found(pixel_id)
        session = db_session.create_session()
        pixel = session.query(Month).get(pixel_id)
        session.delete(pixel)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, pixel_id):
        args = put_parser.parse_args()
        session = db_session.create_session()
        pixel = session.query(Month).get(pixel_id)
        pixel.name = args['name']
        pixel.description = args['description']
        session.commit()
        return jsonify({'success': 'OK'})


class MonthListResource(Resource):
    def get(self):
        session = db_session.create_session()
        pixels = session.query(Month).all()
        return jsonify({'pixels': [item.to_dict(
            only=("id", "color")) for item in pixels]})

    def post(self):
        args = post_parser.parse_args()
        session = db_session.create_session()
        pixel = Month(
            color=args['color'],
        )
        session.add(pixel)
        session.commit()
        return jsonify({'success': 'OK'})
