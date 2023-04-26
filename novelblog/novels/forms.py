from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, StringField, RadioField
from flask_wtf.file import FileField, FileAllowed


class NovelForm(FlaskForm):
    title = StringField('Add Title')
    genre = StringField('Add Genre')
    author = StringField('Add Author')
    picture = FileField('Add Novel Image', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Submit')


class CommentForm(FlaskForm):
    feedback = TextAreaField('Add Feedback')
    submit = SubmitField("Submit")

