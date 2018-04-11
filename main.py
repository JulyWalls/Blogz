from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:bloggers@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(500))

    def __init__(self, title, body):
        self.title = title
        self.body = body


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        blog_title = request.form['title']
        blog_content = request.form['content']

        #validation code will go here

        new_blog = Blog(blog_title, blog_content)
        db.session.add(new_blog)
        db.session.commit()

    blogs = Blog.query.all()


    return render_template('homepage.html', blogs=blogs)


if __name__=='__main__':
    app.run()