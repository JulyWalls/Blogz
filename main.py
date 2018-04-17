from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:bloggers@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
app.secret_key = 'y337kGcys&zP3B'


db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(500))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(120))
    password = db.Column(db.String(120))
    blog = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password


@app.route('/blog', methods=['POST', 'GET'])
def index():
    blog_id = request.args.get('id')

    if request.method == 'GET':
        if not blog_id: 
            blogs = Blog.query.all()
            tab_title = "Homepage"
            return render_template('homepage.html', blogs=blogs, tab_title=tab_title)
        else:
            blogs = Blog.query.get(blog_id)
            return render_template('blog.html', blogs=blogs) 
    

@app.route('/newpost', methods=['POST', 'GET'])
def add_blog():

    if request.method == 'POST':
        blog_title = request.form['title']
        blog_content = request.form['content']

        title_error = ""
        content_error = ""

        if not blog_title or blog_title == " ":
            title_error = "Add a title to your blog"
            blog_title = ""

        if  not blog_content or blog_content == " ":
            content_error = "Add some content to your blog"
            blog_content = ""

        if not title_error and not content_error:
            new_blog = Blog(blog_title, blog_content)
            db.session.add(new_blog)
            db.session.commit()
            blogs = Blog.query.get(new_blog.id)

            return render_template('blog.html', blogs=blogs)
        else:
            return render_template('add-blog-form.html', title_error=title_error, content_error=content_error,
            blog_content=blog_content, blog_title=blog_title)


    tab_title = "Add New Blog"
    return render_template('add-blog-form.html', tab_title=tab_title)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            # TODO - "remember" that the user has logged in
            session['username'] = username
            flash("logged in")
            return redirect('/newpost')

        else:
            flash("user password incorrect, or user does not exist", 'error')
    return render_template('login.html')


    return render_template('login.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

        # TODO - validate data

        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            flash('User already exists', 'error')
            return redirect('/signup')

        if password != verify:
            flash('Passwords do not match', 'error')
            return redirect('/signup')

        if username == "" or password == "" or verify == "":
            flash('Some fields are invalid', 'error')
            return redirect('/signup')

        if len(username) < 3 or len(password) < 3:
            flash('Username or password has to be longer than three characters', 'error')
            return redirect('/signup')



        if not existing_user and password == verify:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/newpost')

    return render_template('signup.html')

@app.route('/logout')
def logout():
    del session['username']
    redirect('/blog')



if __name__=='__main__':
    app.run()