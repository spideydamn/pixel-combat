# -*- coding: cp1251 -*-

import os

from flask import Flask, render_template, redirect, make_response, request, jsonify
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from flask_restful import Api

from data import db_session
from data.user.user import User
from data.day.daily_leader_board import DailyLeaderBoard
from data.week.weekly_leader_board import WeeklyLeaderBoard
from data.month.monthly_leader_board import MonthlyLeaderBoard

from forms.user import RegisterForm, LoginForm, EditForm

from data.user import user_resources
from data.day import day_resources
from data.week import week_resources
from data.month import month_resources

import datetime

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/')
def index():
    return render_template("index.html", title="PixelCombat")


@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    form = RegisterForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.username == form.username.data).first():
            return render_template('sign-up.html', title='PixelCombat | Sign up',
                                   form=form,
                                   message="this username is already taken")
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('sign-up.html', title='PixelCombat | Sign up',
                                   form=form,
                                   message="this user already exists")
        if form.password.data != form.password_again.data:
            return render_template('sign-up.html', title='PixelCombat | Sign up',
                                   form=form,
                                   message="passwords are not equal")
        user = User(username=form.username.data,
                    email=form.email.data)
        user.set_password(form.password.data)
        db_sess.add(user)
        daily_top = DailyLeaderBoard(user=user, number_of_pixels=0)
        db_sess.add(daily_top)
        weekly_top = WeeklyLeaderBoard(user=user, number_of_pixels=0)
        db_sess.add(weekly_top)
        monthly_top = MonthlyLeaderBoard(user=user, number_of_pixels=0)
        db_sess.add(monthly_top)
        db_sess.commit()
        return redirect('/sign-in')
    return render_template('sign-up.html', title='PixelCombat | Sign up', form=form)


@app.route('/sign-in', methods=['GET', 'POST'])
def sign_in():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('sign-in.html',
                               message="wrong email or password",
                               form=form)
    return render_template('sign-in.html', title='PixelCombat | Sign in', form=form)


@app.route('/user', methods=['GET'])
def user():
    id = request.args.get('id', default=0, type=int)
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(id)
    return render_template('user.html',
                           title=f'PixelCombat | {user.username}',
                           username=user.username,
                           id=user.id,
                           created_date=user.created_date.date(),
                           avatar=user.avatar,
                           rank=min(user.daily_top.id, user.weekly_top.id, user.monthly_top.id)
                           )


@login_required
@app.route('/edit', methods=['GET', 'POST'])
def edit():
    form = EditForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if form.username.data != current_user.username and db_sess.query(User).filter(User.username == form.username.data).first():
            return render_template('edit.html', title='PixelCombat | Edit',
                                   form=form,
                                   message="this username is already taken")
        if form.email.data != current_user.email and db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('edit.html', title='PixelCombat | Edit',
                                   form=form,
                                   message="this user already exists")
        if form.old_password.data:
            if not current_user.check_password(form.old_password.data):
                return render_template('edit.html', title='PixelCombat | Edit',
                                       form=form,
                                       message="old password is not equal")
            if form.password.data != form.password_again.data:
                return render_template('edit.html', title='PixelCombat | Edit',
                                       form=form,
                                       message="passwords are not equal")
        user = db_sess.query(User).get(current_user.id)
        if form.username.data != current_user.email:
            user.username = form.username.data
        if form.email.data != current_user.email:
            user.email = form.email.data
        if form.old_password.data and not current_user.check_password(form.password.data):
            user.set_password(form.password.data)
        if form.avatar.data:
            form.avatar.data.save(os.path.join("./static/avatars", f"{current_user.id}.jpg"))
            print(form.avatar.data)
            user.avatar = 1
        db_sess.commit()
        return redirect(f'/user?id={current_user.id}')
    return render_template('edit.html',
                           title=f'PixelCombat | Edit',
                           form=form,
                           rank=min(current_user.daily_top.id, current_user.weekly_top.id, current_user.monthly_top.id))


@app.route('/leader-boards', methods=['GET'])
def leader_boards():
    category = request.args.get('category', default="daily", type=str)
    db_sess = db_session.create_session()
    if category == "daily":
        users = db_sess.query(DailyLeaderBoard).all()
    elif category == "weekly":
        users = db_sess.query(WeeklyLeaderBoard).all()
    elif category == "monthly":
        users = db_sess.query(MonthlyLeaderBoard).all()
    user_list = [[i.user.username, i.number_of_pixels] for i in users]
    return render_template('leader-boards.html',
                           title=f'PixelCombat | {category.capitalize()} Leader Board',
                           users=user_list,
                           category=category
                           )


@app.route('/delete')
@login_required
def delete():
    session = db_session.create_session()
    daily_leader_board = session.query(DailyLeaderBoard).filter(DailyLeaderBoard.user_id == current_user.id).first()
    weekly_leader_board = session.query(WeeklyLeaderBoard).filter(WeeklyLeaderBoard.user_id == current_user.id).first()
    monthly_leader_board = session.query(MonthlyLeaderBoard).filter(MonthlyLeaderBoard.user_id == current_user.id).first()
    session.delete(daily_leader_board)
    session.delete(weekly_leader_board)
    session.delete(monthly_leader_board)
    user = session.query(User).get(current_user.id)
    session.delete(user)
    session.commit()
    return redirect("/")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


def main():
    db_session.global_init("db/PixelCombat.db")
    port = int(os.environ.get("PORT", 5000))
    api.add_resource(user_resources.UserListResource, '/api/user')
    api.add_resource(user_resources.UserResource, '/api/user/<int:user_id>')
    api.add_resource(day_resources.DayListResource, '/api/day')
    api.add_resource(day_resources.DayResource, '/api/day/<int:pixel_id>')
    api.add_resource(week_resources.WeekListResource, '/api/week')
    api.add_resource(week_resources.WeekResource, '/api/week/<int:pixel_id>')
    api.add_resource(month_resources.MonthListResource, '/api/month')
    api.add_resource(month_resources.MonthResource, '/api/month/<int:pixel_id>')
    app.run(host='0.0.0.0', port=port)


if __name__ == '__main__':
    main()