from flask import Flask, request, redirect, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_to_database, Blogger, BlogPost, Tag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///blogly"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'ihaveasecret'

# Uncomment the following line to turn off Debug Toolbar redirects
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

connect_to_database(app)
db.create_all()


@app.route('/')
def homepage():
    """Show a list of recent blog posts, most recent first."""
    blog_posts = BlogPost.query.order_by(BlogPost.created_at.desc()).limit(5).all()
    return render_template("posts/homepage.html", blog_posts=blog_posts)


@app.errorhandler(404)
def not_found_error(e):
    """Show a 404 NOT FOUND page."""
    return render_template('404.html'), 404


# User routes
@app.route('/bloggers')
def list_bloggers():
    """Show a page with information on all bloggers."""
    bloggers = Blogger.query.order_by(Blogger.last_name, Blogger.first_name).all()
    return render_template('bloggers/list.html', bloggers=bloggers)


@app.route('/bloggers/new', methods=["GET"])
def create_blogger_form():
    """Show a form to create a new blogger."""
    return render_template('bloggers/new.html')


@app.route("/bloggers/new", methods=["POST"])
def create_blogger():
    """Handle form submission for creating a new blogger."""
    new_blogger = Blogger(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        image_url=request.form['image_url'] or None)

    db.session.add(new_blogger)
    db.session.commit()
    flash(f"Blogger {new_blogger.full_name} added.")
    return redirect("/bloggers")


@app.route('/bloggers/<int:blogger_id>')
def show_blogger(blogger_id):
    """Show a page with information on a specific blogger."""
    blogger = Blogger.query.get_or_404(blogger_id)
    return render_template('bloggers/show.html', blogger=blogger)


# Add/Edit/Delete Blogger routes are similar to the User routes, just change the names


# Blog Post routes
@app.route('/bloggers/<int:blogger_id>/blog_posts/new')
def create_blog_post_form(blogger_id):
    """Show a form to create a new blog post for a specific blogger."""
    blogger = Blogger.query.get_or_404(blogger_id)
    tags = Tag.query.all()
    return render_template('blog_posts/new.html', blogger=blogger, tags=tags)


# Add/Edit/Delete Blog Post routes are similar to the User routes, just change the names


# Tag routes
@app.route('/tags')
def list_tags():
    """Show a page with information on all tags."""
    tags = Tag.query.all()
    return render_template('tags/list.html', tags=tags)


# Add/Edit/Delete Tag routes are similar to the User routes, just change the names


if __name__ == "__main__":
    app.run(debug=True)
