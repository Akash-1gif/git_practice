from flask import Flask,request,render_template,redirect
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import smtplib
from email.mime.text import MIMEText
import json


app = Flask(__name__)
x='homo sapiens'

with open('config.json','r') as c:
    params=json.load(c)["params"]

with open('config.json','r') as c: 
    metadata=json.load(c)["metadata"]

with open('config.json','r') as c:
    credentials=json.load(c)["credentials"]

local_server_1=True

if (local_server_1==True):
    app.config['SQLALCHEMY_DATABASE_URI']=params["local_uri"]
else:
    app.config['SQLALCHEMY_DATABASE_URI']=params["prod_uri"]


app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)
app.app_context().push()

class Confess(db.Model):
    sno=db.Column(db.Integer, primary_key=True)
    confess_c=db.Column(db.Text,nullable=False)
    date=db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self)->str:
        return f"{self.sno}"
    

class Contact(db.Model):
    sno=db.Column(db.Integer, primary_key=True)
    name_c=db.Column(db.String(30),nullable=False)
    email_c=db.Column(db.String(50),nullable=False)
    subject_c=db.Column(db.String(255),nullable=False)
    message_c=db.Column(db.Text,nullable=False)

    def __repr__(self)->str:
        return f"{self.sno}-{self.subject_c}"    
    
class Posts(db.Model):
    sno=db.Column(db.Integer, primary_key=True)
    post_title=db.Column(db.String(255),nullable=False)
    date_of_publishing=db.Column(db.DateTime,default=datetime.utcnow)
    context=db.Column(db.Text,nullable=False)

    def __repr__(self)->str:
        return f"{self.sno}-{self.post_title}"   
    
db.create_all()

@app.route('/')
def entry_point1():
    return render_template('index.html',name_x=x,index_bio=metadata["index_bio"])

@app.route('/about')
def entry_point_about():
    return render_template('about.html')

@app.route('/confess',methods=['GET','POST'])
def entry_point_confess():
    if request.method=='POST':
        confess=request.form['confess']
        date_time=datetime.utcnow()
        entry=Confess(confess_c=confess, date=date_time)
        # Add the new entry to the database and commit the changes
        db.session.add(entry)
        db.session.commit()
        #notification
        server=smtplib.SMTP('smtp.outlook.com',587)
        server.starttls()
        server.login(credentials["server_email"],credentials["password"])
        msg=MIMEText(confess)
        msg['Subject']="You have a confession"
        msg['From']=credentials["server_email"]
        msg['To']=credentials["recepient_email"]
        msg.set_param('importance','high value')
        server.sendmail(credentials["server_email"],credentials["recepient_email"],msg.as_string())
        


    return render_template('confess.html',confess_info=metadata["confess_info"])

@app.route('/contact',methods=['GET','POST'])
def entry_point_contact():
    if request.method=="POST":
        name=request.form['name']
        email=request.form['email']
        subject=request.form['subject']
        message=request.form['message']
        entry=Contact(name_c=name,email_c=email,subject_c=subject,message_c=message)
        # Add the new entry to the database and commit the changes
        db.session.add(entry)
        db.session.commit()
        sub='You have a new message from blog'
        msg=f'''
Sender's name: {name}
Sender's email: {email}
Sender's subject: {subject}
Sender's message: {message}
        '''
        server=smtplib.SMTP('smtp.outlook.com',587)
        server.starttls()
        server.login(credentials["server_email"],credentials["password"])
        msg=MIMEText(msg)
        msg['Subject']=sub
        msg['From']=credentials["server_email"]
        msg['To']=credentials["recepient_email"]
        msg.set_param('importance','high value')
        server.sendmail(credentials["server_email"],credentials["recepient_email"],msg.as_string())

        

    return render_template('contact.html',contact_info=metadata["contact_info"])

@app.route('/posts')
def entry_point_posts():
    return render_template('posts.html')

@app.route('/works')
def entry_point_works():
    return render_template('works.html')

if __name__ == '__main__':
    app.run()