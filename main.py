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
            return redirect('/blog')
        else:
            return render_template('add-blog-form.html', title_error=title_error, content_error=content_error,
            blog_content=blog_content, blog_title=blog_title)


    tab_title = "Add New Blog"
    return render_template('add-blog-form.html', tab_title=tab_title)



if __name__=='__main__':
    app.run()