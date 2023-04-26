from novelblog import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(64))

    feedback = db.relationship('Comments', backref='author', lazy=True)

    like_user = db.relationship('Like', backref='like_user', lazy='dynamic', foreign_keys='Like.user_id')

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"Username: {self.username}"

    def like_novel(self, novel):
        if not self.has_liked_novel(novel):
            like = Like(user_id=self.id, novel_id=novel.id)
            db.session.add(like)

    def unlike_novel(self, novel):
        if self.has_liked_novel(novel):
            Like.query.filter_by(user_id=self.id, novel_id=novel.id).delete()

    def has_liked_novel(self, novel):
        return Like.query.filter(
            Like.user_id == self.id,
            Like.novel_id == novel.id).count() > 0


class Novel(db.Model):
    __tablename__ = "novels"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    genre = db.Column(db.String(64))
    author = db.Column(db.String(64))
    novel_image = db.Column(db.String(64), nullable=False, default='static/images/themurderofrogerackroyd.jpeg')

    feedbacks = db.relationship('Comments', backref='feedbacks', lazy=True)

    like_novel = db.relationship('Like', backref='like_novel', lazy='dynamic', foreign_keys='Like.novel_id')

    def __init__(self, title, genre, author, novel_image):
        self.title = title
        self.genre = genre
        self.author = author
        self.novel_image = novel_image


class Comments(db.Model):

    users = db.relationship(User)
    novels = db.relationship(Novel)

    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    novel_id = db.Column(db.Integer, db.ForeignKey('novels.id'))
    user_name = db.Column(db.String(64))
    feedback = db.Column(db.Text(100))

    def __init__(self, user_id, novel_id, user_name, feedback):
        self.user_id = user_id
        self.novel_id = novel_id
        self.user_name = user_name
        self.feedback = feedback


class Like(db.Model):
    
    #comments = db.relationship(Comments, foreign_keys=['comments.user_id', 'comments.id'])

    __tablename__ = 'likes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    novel_id = db.Column(db.Integer, db.ForeignKey('novels.id'))
    likeuser = db.relationship(User, foreign_keys=user_id, backref='userlikes', lazy=True)
    likenovel = db.relationship(Novel, foreign_keys=novel_id, backref='novellikes', lazy=True) 

    def __init__(self, user_id, novel_id):
        self.user_id = user_id
        self.novel_id = novel_id
