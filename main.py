from flask import Flask, render_template, request, session, redirect, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:kasey@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = "123456"

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1200))

    def __init__(self, title, body):
        self.title = title
        self.body = body

    def is_valid(self):
        if self.title and self.body:
            return True
        else:
            return False



@app.route('/', methods=['POST', 'GET'])
def index():

    blogs = Blog.query.all()

    return render_template('index.html', title="BLOG", blogs=blogs)

@app.route('/new_post', methods=['POST', 'GET'])
def new_post():

    if request.method == 'POST':

        blog_name = request.form['blog']
        blog_body = request.form['body']

        new_blog = Blog(blog_name, blog_body)

        if new_blog.is_valid():
            db.session.add(new_blog)
            db.session.commit()

            url = "/single_template?id=" + str(new_blog.id)

            return redirect(url)

        else:
            flash("Please add a title.")

            return render_template('new_post.html',
                                    blog_name=blog_name,
                                    blog_body=blog_body)


    else:
        return render_template('new_post.html')



@app.route('/single_template', methods=['GET'])
def single_template():

    blog_id = request.args.get('id')
    blogs = Blog.query.filter_by(id=blog_id).first()

    return render_template('single_template.html', blogs=blogs)


if __name__ == "__main__":
    app.run()