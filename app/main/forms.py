from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, TextField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length


class BlogPostForm(FlaskForm):
    title = StringField('Blog title', validators=[
                        DataRequired(), Length(min=2, max=100)])
    content = TextField('Write New Blog Here', validators=[
        DataRequired(), Length(min=2, max=2000)])
    category = SelectField('Category', choices=[
                           ('Art', 'Art'), ('Business', 'Business'), ('Medicine', 'Medicine'), ('Music', 'Music')])
    submit = SubmitField('Publish')
    image = StringField('Upload an image')


class BlogEditForm(FlaskForm):
    blog_id = StringField()
    title = StringField('Blog title', validators=[
                        DataRequired(), Length(min=2, max=100)])
    edit_content = TextField('Edit Blog', validators=[
        DataRequired(), Length(min=2, max=2000)])
    category = SelectField('Category', choices=[
                           ('Art', 'Art'), ('Business', 'Business'), ('Medicine', 'Medicine'), ('Music', 'Music')])
    submit = SubmitField('Publish')


class CommentForm(FlaskForm):
    content = TextAreaField('Comment', validators=[DataRequired()])
    blog_id = StringField()
    submit = SubmitField('post')


class DeletePost(FlaskForm):
    post_id = StringField('')
    submit = SubmitField('delete')


class DeleteComment(FlaskForm):
    comment_id = StringField('')
    submit = SubmitField('delete')


class LikeShit(FlaskForm):
    blog_id = StringField()
    submit_like = SubmitField('Likes')


class DislikeShit(FlaskForm):
    blog_id = StringField()
    submit_dislike = SubmitField('Dislikes')