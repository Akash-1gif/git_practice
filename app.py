from flask import Flask,request,render_template,redirect
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
x='homo sapiens'

app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///confess.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)
app.app_context().push()

class Confess(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    confess_c = db.Column(db.Text,nullable=False)
    date = db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self)->str:
        return f"{self.sno}"

@app.route('/')
def entry_point1():
    return render_template('index.html',name_x=x)

@app.route('/about')
def entry_point_about():
    return render_template('about.html')

@app.route('/confess',methods=['GET','POST'])
def entry_point_confess():
    if request.method=='POST':
        confess = request.form['confess']
        date_time = datetime.utcnow()
        entry = Confess(confess_c=confess, date=date_time)

        # Add the new entry to the database and commit the changes
        db.session.add(entry)
        db.session.commit()


    return render_template('confess.html')

@app.route('/contact',methods=['GET','POST'])
def entry_point_contact():
    if request.method=="POST":
        name=request.form['name']
        email=request.form['email']
        subject=request.form['subject']
        message=request.form['message']
        print(f'{name}\n{email}\n{subject}\n{message}\n')

    return render_template('contact.html')

@app.route('/posts')
def entry_point_posts():
    return render_template('posts.html')

@app.route('/works')
def entry_point_works():
    return render_template('works.html')

if __name__ == '__main__':
    app.run()