
import os

from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from website import db
from werkzeug.utils import secure_filename
from .models import Post, User


# Create Blueprint
views = Blueprint('views', __name__)


# Home Page
@views.route("/")
def home_Page():

    all_posts = Post.query.order_by(Post.id.desc()).all()

    return render_template(
        "home.html",
        navbar=True,
        user=all_posts
    )


# Blog Page - Display All Posts
@views.route("/blog")
def blog_Page():

    all_posts = Post.query.order_by(Post.id.desc()).all()

    return render_template(
        "blog.html",
        navbar=True,
        user=all_posts
    )


# About Page
@views.route("/about")
def about_Page():

    return render_template(
        "about.html",
        navbar=True
    )


# Contact Page
@views.route("/contact")
def contact_Page():

    return render_template(
        "contact.html",
        navbar=True
    )


# Create Post Page
@views.route("/post", methods=['GET', 'POST'])
@login_required
def post_Page():

    if request.method == "POST":

        # Get Data From Form
        title = request.form.get("titleBlog")
        tag = request.form.get("tags")
        content = request.form.get("content")

        # Get Image
        img = request.files.get("thumb")

        if not title or not tag or not content:
            return render_template(
                "post.html",
                navbar=False,
                user=current_user,
                error=True
            )

        if not img or not img.filename:
            return render_template(
                "post.html",
                navbar=False,
                user=current_user,
                error=True
            )

        # Secure Image Name
        img_name = secure_filename(img.filename)

        # Upload Folder
        upload_folder = os.path.join(
            os.getcwd(),
            "website",
            "static",
            "img"
        )

        os.makedirs(upload_folder, exist_ok=True)

        # Save Image
        img.save(os.path.join(upload_folder, img_name))

        # Create Post
        post = Post(
            title=title,
            tag=tag,
            img=img_name,
            content=content,
            user_id=current_user.id
        )

        # Save To Database
        db.session.add(post)
        db.session.commit()

        # Redirect To Blog
        from flask import redirect, url_for

        return redirect(url_for("views.blog_Page"))

    return render_template(
        "post.html",
        navbar=False,
        user=current_user
    )


# Single Blog Post
@views.route('/blog/<int:id>/<int:user_id>/<string:title>')
def blogs(id, user_id, title):

    # Get Post
    post = Post.query.filter_by(
        id=id,
        user_id=user_id
    ).first_or_404()

    # Get Author
    author = User.query.filter_by(
        id=post.user_id
    ).first()

    return render_template(
        "blogPost.html",
        navbar=True,
        user=post,
        author=author.user_name if author else "Unknown"
    )
