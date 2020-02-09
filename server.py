from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_email import send_email
from sqlalchemy.sql import func
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]='postgres://uylzffflwlpcpr:074641a717f66bedd71e22db51627f482b68229d2083d15c1d033588924ec561@ec2-3-234-169-147.compute-1.amazonaws.com:5432/d3fk4buvimibm2?sslmode=require'
db = SQLAlchemy(app)


class Data(db.Model):
    __tablename__ = "data"
    id = db.Column(db.Integer, primary_key=True)
    email_ = db.Column(db.String(80), unique=True)
    height_ = db.Column(db.Integer)
    
    def __init__(self, email_, height_):
        self.email_ = email_
        self.height_ = height_


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/success', methods=['POST', 'GET'])
def success():
    if request.method == 'POST':
        email = request.form['email']
        height = request.form['height']

        if db.session.query(Data).filter(Data.email_ == email).count() != 1:
            data = Data(email, height)
            db.session.add(data)
            db.session.commit()
            avg_height = db.session.query(func.avg(Data.height_)).scalar()
            avg_height = round(avg_height, 2)
            count = db.session.query(Data.height_).count()
            send_email(email, height, avg_height, count)

            return render_template('success.html')
    return render_template('index.html', text=" Your Email Id already exist")


if __name__ == '__main__':
    app.run(debug=True)