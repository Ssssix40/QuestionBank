from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_nav import Nav
from flask_nav.elements import Navbar, View
from flask_paginate import Pagination, get_page_parameter
from flask_bootstrap import Bootstrap
import config
import re

app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)
Bootstrap(app)
nav = Nav()
nav.register_element(
    'top',
    Navbar(u'题库', View(u"搜索", "index"), View(u"所有", "all"),
           View(u"常识判断", "types", mtype=u"a"),
           View(u"言语理解与表达", "types", mtype=u"b"),
           View(u"数量关系", "types", mtype=u"c"),
           View(u"判断推理", "types", mtype=u"d"),
           View(u"资料分析", "types", mtype=u"e")))

nav.init_app(app)


class Questions(db.Model):
    __tablename__ = 'Questions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Means = db.Column(db.Text)
    Title = db.Column(db.String(2500))
    Answers = db.Column(db.String(2500))
    CAnswers = db.Column(db.String(2500))
    Statistics = db.Column(db.String(2500))
    Analysis = db.Column(db.Text)
    Point = db.Column(db.String(2500))
    Source = db.Column(db.String(2500))


def questionsSort(questions, title):
    questionsDict = {}
    for i in questions:
        number = re.search(r"\d+", i.Title).group()
        sources = i.Source.split("、")
        for j in sources:
            if number in j and title in j:
                questionsDict[int(number)] = i
    newQuestions = []
    for i in sorted(questionsDict):
        newQuestions.append(questionsDict[i])
    return newQuestions


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        indexpath = request.form['searcher']
        radio = request.form['choicer']
        radio = int(radio)
        return redirect(url_for("search", catage=radio, keys=indexpath))
    questions = []

    return render_template("search.html", questions=questions)


@app.route('/search/<catage>/<keys>', methods=['GET', 'POST'])
def search(catage, keys):
    if request.method == 'POST':
        indexpath = request.form['searcher']
        radio = request.form['choicer']
        radio = int(radio)
        return redirect(url_for("search", catage=radio, keys=indexpath))

    if catage == "1" or catage == "2":
        if catage == "1":
            questions = Questions.query.filter(
                Questions.Title.contains(keys)).all()
        elif catage == "2":
            questions = Questions.query.filter(
                Questions.Point.contains(keys)).all()
        page = request.args.get(get_page_parameter(), type=int, default=1)
        search = False
        total = len(questions)
        questions = questions[(page - 1) * 10:(page - 1) * 10 + 10]
        pagination = Pagination(page=page,
                                total=total,
                                search=search,
                                record_name='questions',
                                bs_version=4)
        return render_template("searchNormal.html",
                               questions=questions,
                               pagination=pagination)
    elif catage == "3":
        questions = Questions.query.filter(
            Questions.Source.contains(keys)).all()
        questions = questionsSort(questions, keys)
        return render_template("search.html", questions=questions)
    # else:
    #     questions = []

    # return render_template("search.html", questions=questions)


@app.route('/all')
def all():
    search = False
    # q = request.args.get('q')
    # if q:
    #     search = True

    page = request.args.get(get_page_parameter(), type=int, default=1)

    total = len(Questions.query.all())
    questions = Questions.query.slice((page - 1) * 10, (page - 1) * 10 + 10)
    pagination = Pagination(page=page,
                            total=total,
                            search=search,
                            record_name='questions',
                            bs_version=4)
    return render_template("index.html",
                           questions=questions,
                           pagination=pagination,
                           mtype="所有题目")


@app.route("/types/<mtype>")
def types(mtype):
    typeDic = {
        "a": "常识判断",
        "b": "言语理解与表达",
        "c": "数量关系",
        "d": "判断推理",
        "e": "资料分析"
    }
    search = False

    page = request.args.get(get_page_parameter(), type=int, default=1)
    questions = Questions.query.filter(Questions.Point.contains(
        typeDic[mtype]))
    total = questions.count()
    questions = questions[(page - 1) * 10:(page - 1) * 10 + 10]
    pagination = Pagination(page=page,
                            total=total,
                            search=search,
                            record_name='questions',
                            bs_version=4)
    return render_template("index.html",
                           questions=questions,
                           pagination=pagination,
                           mtype=typeDic[mtype])


@app.route("/edit/<questionID>", methods=['GET', 'POST'])
def edit(questionID):
    if request.method == 'POST':
        question = Questions.query.filter_by(id=request.form['Id']).first()
        question.Means = request.form['Means']
        question.Title = request.form['Title']
        question.Answers = request.form['Answers']
        question.CAnswers = request.form['CAnswers']
        question.Statistics = request.form['Statistics']
        question.Analysis = request.form['Analysis']
        question.Point = request.form['Point']
        question.Source = request.form['Source']
        db.session.commit()

    question = Questions.query.get(questionID)
    return render_template("edit.html", question=question)


@app.route("/download/<examName>")
def download(examName):
    return "%s" % examName


if __name__ == '__main__':
    app.debug = True
    app.run()
