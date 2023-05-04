import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from data.db_session import SqlAlchemyBase


class DailyLeaderBoard(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'dailyleaderboard'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey('user.id'), nullable=False)
    user = orm.relationship('User', back_populates="daily_top")
    number_of_pixels = sqlalchemy.Column(sqlalchemy.Integer, default=0)
