from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import func
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import matplotlib.pyplot as plt
import re

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///questionaire_test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text)
    surname = db.Column(db.Text)
    age = db.Column(db.Integer)
    gender = db.Column(db.Text)
    city = db.Column(db.Text)


class Questions(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)


class Answers(db.Model):
    __tablename__ = 'answers'
    answer_id = db.Column("answer_id", db.Integer, primary_key=True)
    q1 = db.Column("q1", db.Text)
    q2 = db.Column("q2", db.Text)
    q3 = db.Column("q3", db.Text)
    q4 = db.Column("q4", db.Text)
    q5 = db.Column("q5", db.Text)
    q6 = db.Column("q6", db.Text)
    q7 = db.Column("q7", db.Text)
    q8 = db.Column("q8", db.Text)
    q9 = db.Column("q9", db.Text)

# сделать то же с вопросами, если они будут в таблице:
# class Questions(db.Model):
#     __tablename__ = 'questions'
#     question_id = db.Column("question_id", db.Integer, primary_key=True)
#     text = db.Column("question", db.Text)


@app.route('/')  # главная страница
def index():
    return render_template("index.html")


@app.route('/questionaire')  # страница анкеты
def question_page():
#  questions = Questions.query.all()
    return render_template(
        'quest.html',
#  questions=questions
    )


@app.route(rule='/results', methods=['get'])
def answer_process():
    if not request.args:
        return redirect(url_for('/'))
    age = request.args.get('age')
    gender = request.args.get('gender')
    city = request.args.get('city')
    if len(User.query.all()) == 0:
        last_user = -1
    else:
        last_user = User.query.all()[-1].user_id
    user = User(
        user_id=last_user + 1,
        age=int(age),
        gender=gender,
        city=city
    )
    db.session.add(user)
    db.session.commit()
    db.session.refresh(user)
    q1 = request.args.get("q1")
    q2 = request.args.get("q2")
    q3 = request.args.get("q3")
    q4 = request.args.get("q4")
    q5 = request.args.get("q5")
    q6 = request.args.get("q6")
    q7 = request.args.get("q7")
    q8 = request.args.get("q8")
    q9 = request.args.get("q9")
    answer = Answers(answer_id=user.user_id, q1=q1, q2=q2,
    q3=q3, q4=q4, q5=q5, q6=q6, q7=q7, q8=q8, q9=q9)
    db.session.add(answer)
    db.session.commit()
    return redirect(url_for("stats"))


@app.route('/stats')
def stats():
    all_info = {}
    age_stats = db.session.query(
        func.avg(User.age),
        func.min(User.age),
        func.max(User.age)
    ).one()
    all_info['age_mean'] = age_stats[0]
    all_info['age_min'] = age_stats[1]
    all_info['age_max'] = age_stats[2]
    all_info['total_count'] = User.query.count()

    q1_answers = db.session.query(Answers.q1).all()
    q2_answers = db.session.query(Answers.q2).all()
    q3_answers = db.session.query(Answers.q3).all()
    q4_answers = db.session.query(Answers.q4).all()
    q5_answers = db.session.query(Answers.q5).all()
    q6_answers = db.session.query(Answers.q6).all()
    q7_answers = db.session.query(Answers.q7).all()
    q8_answers = db.session.query(Answers.q8).all()
    q9_answers = db.session.query(Answers.q9).all()
    gender_answers = db.session.query(User.gender).all()

    stat_df = pd.DataFrame({'Вопрос 1': q1_answers, 'Вопрос 2': q2_answers, 'Вопрос 3': q3_answers,
    'Вопрос 4': q4_answers, 'Вопрос 5': q5_answers, 'Вопрос 6': q6_answers, 'Вопрос 7': q7_answers,
    'Вопрос 8': q8_answers, 'Вопрос 9': q9_answers, 'Гендер': gender_answers})
    q1_info = stat_df["Вопрос 1"].value_counts()
    all_info["q1_freq"] = q1_info.max()
    q1_freq = q1_info.idxmax()
    all_info["q1_freq_ans"] = re.sub(r'[^\w\s]', '', str(q1_freq))
    stat_df['Вопрос 1'].value_counts().plot.pie()
    save_path = "static/diagram.png"
    plt.savefig(save_path)

    return render_template('stats.html', all_info=all_info)


if __name__ == '__main__':
    app.run()

