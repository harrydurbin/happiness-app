import os
from flask import Flask, render_template, session, redirect, url_for
from flask_script import Manager, Shell
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import Required
from flask_sqlalchemy import SQLAlchemy
import pickle
import numpy as np
import random


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'asdfjlkkasdf'
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)

# note: in shell create db with db.create_all()

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    # username = db.Column(db.String(64), unique=True, index=True)
    health = db.Column(db.Integer)
    householdfinances = db.Column(db.Integer)
    neighborrace = db.Column(db.Integer)
    neighborimmigrant = db.Column(db.Integer)
    neighbordiffreligion = db.Column(db.Integer)
    neighborunmarriedcpl = db.Column(db.Integer)
    lifecontrol = db.Column(db.Integer)
    neighborhoodsecurity = db.Column(db.Integer)
    countryhumanrights = db.Column(db.Integer)
    incomescale = db.Column(db.Integer)
    socclass = db.Column(db.Integer)
    leisureimport = db.Column(db.Integer)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    # def __repr__(self):
    #     return '<User %r>' % self.username


class NameForm(FlaskForm):
    # name = StringField('What is your name?', validators=[Required()])

    health = SelectField(u'All in all, how would you describe your state of health these days',
        choices=[(1,'1 : Very Good'),(2,'2 : Good'),(3,'3 : Fair'),(4,'4 : Poor')], coerce=int)

    householdfinances = SelectField(u'How satisfied are you with the financial situation of your household?',
        choices=[(1,'1 : Completely disatisfied'),(2,'2'),(3,'3'),(4,'4'),(5,'5'),(6,'6'),(7,'7'),(8,'8'),(9,'9'),(10,'10: Completely satisfied')], coerce=int)

    neighborrace = SelectField(u'Could you please mention if you would not like to have as neighbors ...People of another race',
        choices=[(1,'1 : Would not like'),(2,'2 : Does not matter')], coerce=int)

    neighborimmigrant = SelectField(u'...People who are immigrants/foreign',
        choices=[(1,'1 : Would not like'),(2,'2 : Does not matter')], coerce=int)

    neighbordiffreligion =  SelectField(u'...People who are are different religion',
        choices=[(1,'1 : Would not like'),(2,'2 : Does not matter')], coerce=int)

    neighborunmarriedcpl = SelectField(u'...People who are an unmarried couple living together',
        choices=[(1,'1 : Would not like'),(2,'2 : Does not matter')], coerce=int)

    lifecontrol = SelectField(u'Some people feel they have completely free choice and control over their lives, while other people feel that what they do has no real effect on what happens to them. Please indicate how much freedom of choice and control you feel you have over the way your life turns out.',
        choices=[(1,'1 : No choice at all'),(2,'2'),(3,'3'),(4,'4'),(5,'5'),(6,'6'),(7,'7'),(8,'8'),(9,'9'),(10,'10: A great deal of choice')], coerce=int)

    neighborhoodsecurity = SelectField(u'Could you tell me how secure do you feel these days in your neighborhood?',
        choices=[(1,'1 : Very secure'),(2,'2 : Quite secure'),(3,'3 : Not very secure'), (4,'4 : Not at all secure')], coerce=int)

    countryhumanrights = SelectField(u'How much respect is there for individual human rights nowadays in this country? Do you feel there is:',
        choices=[(1,'1 : A great deal of respect for individual human rights'),(2,'2 : Fairly much respect'),(3,'3 : Not much respect'), (4,'4 : No respect at all')], coerce=int)

    incomescale = SelectField(u'An income scale on which 1 indicates the lowest income group and 10 the highest income group in your country. Please specify the appropriate number, counting all incomes that come in.',
        choices=[(1,'1 : Lowest group'),(2,'2'),(3,'3'),(4,'4'),(5,'5'),(6,'6'),(7,'7'),(8,'8'),(9,'9'),(10,'10: Highest group')], coerce=int)

    socclass = SelectField(u'People sometimes describe themselves as belonging to the working class, the middle class, or the upper or lower class. Would you describe yourself as belonging to the:',
        choices=[(1,'1 : Upper class'),(2,'2 : Upper middle class'),(3,'3 : Lower middle class'), (4,'4 : Working class'),(5,'5 : Lower class')], coerce=int)

    leisureimport = SelectField(u'Indicate how important leisure time is in your life:',
        choices=[(1,'1 : Very important'),(2,'2 : Rather important'),(3,'3 : Not very important'), (4,'4 : Not at all important')], coerce=int)

    submit = SubmitField('Submit')


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)
manager.add_command("shell", Shell(make_context=make_shell_context))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/survey', methods=['GET', 'POST'])
def survey():
    form = NameForm()
    if form.validate_on_submit():

        # username=form.name.data
        health=form.health.data
        householdfinances = form.householdfinances.data
        neighborrace = form.neighborrace.data
        neighborimmigrant = form.neighborimmigrant.data
        neighbordiffreligion = form.neighbordiffreligion.data
        neighborunmarriedcpl = form.neighborunmarriedcpl.data
        lifecontrol = form.lifecontrol.data
        neighborhoodsecurity = form.neighborhoodsecurity.data
        countryhumanrights = form.countryhumanrights.data
        incomescale = form.incomescale.data
        socclass = form.socclass.data
        leisureimport = form.leisureimport.data

        user = User(health=health, householdfinances=householdfinances,
                    neighborrace=neighborrace, neighborimmigrant=neighborimmigrant,
                    neighbordiffreligion=neighbordiffreligion,neighborunmarriedcpl=neighborunmarriedcpl,
                    lifecontrol=lifecontrol,neighborhoodsecurity=neighborhoodsecurity,
                    countryhumanrights=countryhumanrights,incomescale=incomescale,socclass=socclass,
                    leisureimport=leisureimport)

        db.session.add(user)

        # session['name'] = username
        session['health'] = health
        session['householdfinances'] = householdfinances
        session['neighborrace'] = neighborrace
        session['neighborimmigrant'] = neighborimmigrant
        session['neighbordiffreligion'] = neighbordiffreligion
        session['neighborunmarriedcpl'] = neighborunmarriedcpl
        session['lifecontrol'] = lifecontrol
        session['neighborhoodsecurity'] = neighborhoodsecurity
        session['countryhumanrights'] = countryhumanrights
        session['incomescale'] = incomescale
        session['socclass'] = socclass
        session['leisureimport'] = leisureimport

        pkl_filename = 'classifier.pkl'
        model_pkl = open(pkl_filename, 'rb')
        clf = pickle.load(model_pkl, encoding = 'latin1')

        feats = [health, householdfinances, neighborrace, neighborimmigrant,
        leisureimport, lifecontrol, neighborhoodsecurity, countryhumanrights,
        incomescale, socclass, neighbordiffreligion, neighborunmarriedcpl]

        feats = np.asarray(feats)
        feats = feats.reshape(1,-1)

        prediction = clf.predict(feats)

        pred_dict = {1: 'VERY HAPPY. I hope it is correct.',\
        2: 'RATHER HAPPY. I hope you are even happier than my prediction.',\
        3: 'NOT VERY HAPPY. I hope my prediction is wrong and you actually feel happier than I guessed. Situations can sometimes suck. If you feel you need more peace, maybe you could try daily meditation.',\
        4: 'NOT AT ALL HAPPY. I hope my prediction is wrong and you actually feel happier than I guessed. Situations can sometimes suck. If you feel you need more peace, maybe you could try daily meditation.'}

        session['prediction'] = pred_dict[prediction[0]]
        return redirect(url_for('results'))

    return render_template('survey.html', form=form)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/results')
def results():

    quotes = ["'The very purpose of our life is to seek happiness.'  --the Dalai Lama",
            "'Happiness depends on ourselves.'  --Aristotle",
            "'For every minute you are angry you lose sixty seconds of happiness.'  --Ralph Waldo Emerson",
            "'Folks are usually about as happy as they make their minds up to be.'  --Abraham Lincoln",
            "'I have decided to be happy because it is good for my health.'  --Voltaire",
            "'Have only love in your heart for others. The more you see the good in them, the more you will establish good in yourself' --Paramahansa Yogananda",
            "'Happiness is when what you think, what you say, and what you do are in harmony.'  --Mahatma Gandhi"]

    i = random.randint(0,len(quotes)-1)

    return render_template('results.html',prediction=session.get('prediction'), quote=quotes[i])


if __name__ == '__main__':
    manager.run()
