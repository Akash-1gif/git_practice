from flask import Flask,request,render_template,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///posts.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)
app.app_context().push()

class Posts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255),nullable=False)
    content = db.Column(db.LONGTEXT,nullable=False)
    date = db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self)->str:
        return f"{self.title} - {self.date}"

x='homo sapiens'

@app.route('/')
def entry_point1():
    return render_template('index.html',name_x=x)

@app.route('/about')
def entry_point_about():
    return render_template('about.html')

@app.route('/confess')
def entry_point_confess():
    return render_template('confess.html')

@app.route('/contact')
def entry_point_contact():
    return render_template('contact.html')

@app.route('/posts')
def entry_point_posts():
    return render_template('posts.html')

@app.route('/works')
def entry_point_works():
    return render_template('works.html')

if __name__ == '__main__':
    app.run(debug=True)