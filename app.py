import os
from datetime import datetime
from flask import Flask,url_for,redirect,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import StringField,DateField,SelectField,SubmitField,TextAreaField
from wtforms.validators import Email,DataRequired
from values import *
from flask_mail import Mail,Message

app = Flask(__name__)

app.config["SECRET_KEY"] = "somesecretkey"
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(basedir,'database.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL')
app.config['MAIL_PASSWORD'] = os.environ.get('PASS')

db = SQLAlchemy(app)
Migrate(app,db)

mail = Mail(app)

class Appointment(db.Model):
    __tablename__ = "appointments"
    id = db.Column(db.Integer,primary_key=True)
    date = db.Column(db.DateTime,nullable=False)
    dept = db.Column(db.String,nullable=False)
    loc = db.Column(db.String,nullable=False)
    email = db.Column(db.String,nullable=False)
    
    def __init__(self,date,email,dept,loc):
        self.email = email
        self.dept = dept
        self.loc = loc
        self.date = date

class AppointmentForm(FlaskForm):
    email = StringField("Email",[DataRequired(),Email()])
    day = SelectField("Day",[DataRequired()],choices=days())
    month = SelectField("Month",[DataRequired()],choices=month())
    year = SelectField("Year",[DataRequired()],choices=year())
    dept = SelectField("Select department",[DataRequired()],choices=depts())
    loc = SelectField("Location",[DataRequired()],choices=locs())
    submit = SubmitField("Confirm")

class FeedBack(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String,nullable=False)
    comment = db.Column(db.String,nullable=False)

    def __init__(self,name,comment):
        self.name = name
        self.comment = comment

class FeedbackForm(FlaskForm):
    name = StringField("Name",[DataRequired()])
    comment = TextAreaField("Feedback",[DataRequired()])
    submit = SubmitField("Submit")
    
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/appoint',methods=["GET","POST"])
def appointment():
    form = AppointmentForm()
    invalid_date = False
    booked = False
    invalid_mail = False
    if form.is_submitted():
        current_time = datetime.now()
        try:
            entered = datetime(year=int(form.year.data),month=int(form.month.data),day=int(form.day.data))
            if entered >= current_time:
                appt = Appointment(date=entered,email=form.email.data,dept=form.dept.data,loc=form.loc.data)
                db.session.add(appt)
                db.session.commit()
                msg = Message("Appointment Confirmation",sender= 'admin@lifecarehospitals.com',recipients=[form.email.data])
                msg.body = f"Your appointment with LifeCare, Location {form.loc.data} has been booked for date {entered.strftime('%d-%m-%Y')}.\nRegards,\nTeam LifeCare"
                try:
                    mail.send(msg)
                except:
                    invalid_mail = True
                booked = True
            else:
                invalid_date = True
        except:
            invalid_date = True
    return render_template('book.html',form=form,invalid_date=invalid_date,booked=booked,invalid_mail=invalid_mail)

@app.route('/feedback',methods=["GET","POST"])
def feedback():
    form = FeedbackForm()
    done = False
    if form.validate_on_submit():
        fd = FeedBack(name=form.name.data,comment=form.comment.data)
        db.session.add(fd)
        db.session.commit()
        done = True
    return render_template('feedback.html',form=form,done=done)

@app.route('/locations')
def locations():
    return render_template('locations.html')

if __name__ == "__main__":
    app.run(debug=True)
