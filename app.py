from flask import Flask,request,render_template,redirect

app = Flask(__name__)

x='homo sapiens'

@app.route('/')
def entry_point1():
    return render_template('index.html',name_x=x)

@app.route('/index')
def entry_point_index():
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