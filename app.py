from flask import Flask,request,render_template,redirect
from datetime import datetime

app = Flask(__name__)

x='homo sapiens'

@app.route('/')
def entry_point1():
    return render_template('index.html',name_x=x)

@app.route('/about')
def entry_point_about():
    return render_template('about.html')

@app.route('/confess',methods=['GET','POST'])
def entry_point_confess():
    if request.method=='POST':
        confess=request.form['confess']
        print(f"{confess}")
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