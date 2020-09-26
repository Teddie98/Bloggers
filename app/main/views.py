from . import main
from flask import render_template, redirect, url_for, request
from flask_login import current_user
from ..models import BlogPost, Comment
from .forms import BlogPostForm, CommentForm, DeletePost, BlogEditForm, LikeShit, DislikeShit
from datetime import datetime
from .. import db, photos


@main.route('/', methods=['GET', 'POST'])
def home():
    title = 'This is a blog website'
    blogs = BlogPost.query.all()
    return render_template('index.html', title=title, blogs=blogs)


@main.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    title = 'Dashboard'
    blogs = BlogPost.query.all()
    form = BlogPostForm()
    del_form = DeletePost()
    edit_form = BlogEditForm()

    if edit_form.validate_on_submit():
        path = ''
        print('path')
        print('photoedit' in request.files)
        if 'photoedit' in request.files:
            filename = photos.save(request.files['photoedit'])
            path = f'photos/{filename}'
        blog_title = edit_form.blog_id.data
        edit_blog = BlogPost.query.filter_by(title=blog_title).first()
        edit_blog.title = edit_form.title.data
        edit_blog.content = edit_form.edit_content.data
        edit_blog.category = edit_form.category.data
        edit_blog.image = path
        db.session.commit()
        return redirect(url_for('main.dashboard'))

    elif form.validate_on_submit():
        path = ''
        print('photo' in request.files)
        if 'photo' in request.files:
            filename = photos.save(request.files['photo'])
            path = f'photos/{filename}'
        new_blog = BlogPost(title=form.title.data,
                            content=form.content.data,
                            category=form.category.data,
                            likes=0,
                            dislikes=0,
                            rating=0,
                            image=path,
                            time=datetime.utcnow().strftime("%H:%M"),
                            author=current_user)
        new_blog.save_blog(new_blog)
        return redirect(url_for('main.dashboard'))

    elif del_form.validate_on_submit():
        blog_id = del_form.post_id.data
        del_blog = BlogPost.query.filter_by(title=blog_id).first()
        if del_blog:
            del_blog.delete_blog(del_blog)
            return redirect(url_for('main.dashboard'))
        return redirect(url_for('main.dashboard'))
    return render_template('dashboard.html', title=title, form=form, blogs=blogs, del_form=del_form, edit_form=edit_form)


@main.route('/<title>', methods=['GET', 'POST'])
def article(title):
    print(title)
    form = CommentForm()
    like = LikeShit()
    dislike = DislikeShit()

    article = BlogPost.query.filter_by(title=title).first()
    if form.validate_on_submit():
        blogs = BlogPost.query.all()
        blog = BlogPost.query.get(int(form.blog_id.data))
        new_comment = Comment(content=form.content.data, likes=0,
                              dislikes=0, time=datetime.utcnow().strftime("%H:%M"), blog=blog, author=current_user)
        new_comment.save_blog(new_comment)
        comments = blog.comments.all()
        return redirect(url_for('main.article', title=title, blogs=blogs,  comments=comments))

    elif like.validate_on_submit():
        article.likes = article.likes + 1
        db.session.commit()
        print('WRONG')

    elif dislike.validate_on_submit():
        article.dislikes = article.dislikes + 1
        db.session.commit()
        print(article.dislikes)

    return render_template('article.html', article=article, form=form, like=like, dislike=dislike)