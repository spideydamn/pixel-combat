import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from data.db_session import SqlAlchemyBase

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'user'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    username = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
    email = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    avatar = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    daily_shaded_pixels = orm.relationship("Day", back_populates='painter')
    weekly_shaded_pixels = orm.relationship("Week", back_populates='painter')
    monthly_shaded_pixels = orm.relationship("Month", back_populates='painter')
    daily_last_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    weekly_last_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    monthly_last_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    daily_top = orm.relationship("DailyLeaderBoard", uselist=False, back_populates="user")
    weekly_top = orm.relationship("WeeklyLeaderBoard", uselist=False, back_populates="user")
    monthly_top = orm.relationship("MonthlyLeaderBoard", uselist=False, back_populates="user")

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
