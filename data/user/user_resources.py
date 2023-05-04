from flask_login import login_required
from flask_restful import Resource, abort
from flask import jsonify

from .. import db_session
from .user import User
from ..day.daily_leader_board import DailyLeaderBoard
from ..week.weekly_leader_board import WeeklyLeaderBoard
from ..month.monthly_leader_board import MonthlyLeaderBoard
from .user_parser import post_parser, put_parser


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")


class UserResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify({'users': user.to_dict(
            only=("id", "username", "email", "created_date", "daily_last_date", "weekly_last_date", "monthly_last_date"))})

    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        daily_leader_board = session.query(DailyLeaderBoard).filter(
            DailyLeaderBoard.user_id == user_id).first()
        weekly_leader_board = session.query(WeeklyLeaderBoard).filter(
            WeeklyLeaderBoard.user_id == user_id).first()
        monthly_leader_board = session.query(MonthlyLeaderBoard).filter(
            MonthlyLeaderBoard.user_id == user_id).first()
        session.delete(daily_leader_board)
        session.delete(weekly_leader_board)
        session.delete(monthly_leader_board)
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, user_id):
        args = put_parser.parse_args()
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        user.username = args['username']
        user.email = args['email']
        user.set_password(args['password'])
        session.commit()
        return jsonify({'success': 'OK'})


class UserListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify({'users': [item.to_dict(
            only=("id", "username", "email", "created_date")) for item in users]})

    def post(self):
        args = post_parser.parse_args()
        session = db_session.create_session()
        user = User(
            username=args['username'],
            email=args['email'],
        )
        user.set_password(args['password'])
        session.add(user)
        daily_top = DailyLeaderBoard(user=user, number_of_pixels=0)
        session.add(daily_top)
        weekly_top = WeeklyLeaderBoard(user=user, number_of_pixels=0)
        session.add(weekly_top)
        monthly_top = MonthlyLeaderBoard(user=user, number_of_pixels=0)
        session.add(monthly_top)
        session.commit()
        return jsonify({'success': 'OK'})


