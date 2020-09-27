from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user
from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30))
    firstname = db.Column(db.String(30))
    lastname = db.Column(db.String(30))
    email = db.Column(db.String(30))
    pass_hash = db.Column(db.String(255))
    bio = db.Column(db.String)
    profile_photo = db.Column(db.String, default='default.jpg')
    blogs = db.relationship('BlogPost', backref='author', lazy='dynamic')
    comments = db.relationship('Comment', backref='author', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('You cant access the password')

    @password.setter
    def password(self, password):
        self.pass_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.pass_hash, password)

    def save_user(self, user):
        db.session.add(user)
        db.session.commit()

    def __repr__(self):
        return f'User {self.id}, {self.username}, {self.email}'


class BlogPost(db.Model):
    __tablename__ = 'blogposts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(4000), nullable=False)
    category = db.Column(db.String(30))
    likes = db.Column(db.Integer)
    dislikes = db.Column(db.Integer)
    rating = db.Column(db.Integer)
    time = db.Column(db.String(50))
    image = db.Column(db.String)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comments = db.relationship('Comment', backref='blog', lazy='dynamic')
    photos = db.relationship('Image', backref='blog', lazy="dynamic")

    def save_blog(self, blog):
        db.session.add(blog)
        db.session.commit()

    def delete_blog(self, blog):
        db.session.delete(blog)
        db.session.commit()

    def save_changes(self, blog):
        db.session.commit()

    def __repr__(self):
        return f'Blog Post {self.id}, {self.title}'


class Image(db.Model):
    __tablename__ = 'photos'

    id = db.Column(db.Integer, primary_key=True)
    pic_path = db.Column(db.String())
    user_id = db.Column(db.Integer, db.ForeignKey("blogposts.id"))


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(4000), nullable=False)
    likes = db.Column(db.Integer)
    dislikes = db.Column(db.Integer)
    time = db.Column(db.String(50))
    blog_id = db.Column(db.Integer, db.ForeignKey('blogposts.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def save_blog(self, blog):
        db.session.add(blog)
        db.session.commit()

    def __repr__(self):
        return f'Blog Post {self.id}, {self.blog}, {self.author}, {self.content}'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))