from flask import abort
from flask import render_template, Blueprint, redirect, url_for, request
from flask_login import login_required, current_user
from novelblog import db
from novelblog.novels.forms import CommentForm, NovelForm
from novelblog.models import Comments, Novel
from novelblog.novels.picture_handler import add_novel_pic

novels = Blueprint('novels', __name__)

@novels.route('/index')
@login_required
def index():
    return render_template('index.html', novels=Novel.query.all())


@novels.route('/addnovel', methods=['GET', 'POST'])
@login_required
def addnovel():
    form = NovelForm()

    if form.validate_on_submit():
        title = form.title.data
        pic = None
        if form.picture.data:
            pic = add_novel_pic(form.picture.data, title)
        novel = Novel(title = title, genre = form.genre.data, author = form.author.data, novel_image = pic)
        db.session.add(novel)
        db.session.commit()

        return render_template('index.html', novels=Novel.query.all())
    return render_template('addnovel.html', form=form, novels=Novel.query.all())


@novels.route('/editnovel/<novelId>', methods=['GET', 'POST'])
@login_required
def editnovel(novelId):
    form = NovelForm()

    novel = Novel.query.filter_by(id = novelId).first()
    if form.validate_on_submit():
        novel.title = form.title.data
        novel.author = form.author.data
        novel.genre = form.genre.data
        pic = novel.novel_image
        if form.picture.data:
            pic = add_novel_pic(form.picture.data, novel.title)
        novel.novel_image = pic
        db.session.commit()

        return redirect(url_for('novels.index'))

    elif request.method == 'GET':
        form.title.data = novel.title
        form.author.data = novel.author
        form.genre.data = novel.genre
        form.picture.data = novel.novel_image

    return render_template('addnovel.html', form=form, novels=Novel.query.all())



@novels.route('/deletenovel/<novelId>', methods=['GET', 'POST'])
@login_required
def deletenovel(novelId):
    novel = Novel.query.filter_by(id = novelId).first()
    db.session.delete(novel)
    db.session.commit()

    return redirect(url_for('novels.index'))


@novels.route('/addfeedback/<novelId>', methods=['GET', 'POST'])
@login_required
def addfeedback(novelId):
    form = CommentForm()

    if form.validate_on_submit():
        comment = Comments(user_id = current_user.id, novel_id = novelId, user_name = current_user.username, feedback=form.feedback.data)
        db.session.add(comment)
        db.session.commit()

        return redirect(url_for('novels.addfeedback', novelId=novelId))
    return render_template('addfeedback.html', form=form, feedback=Comments.query.filter_by(novel_id = novelId).all(), count=Comments.query.filter_by(novel_id = novelId).count())


@novels.route('/deletefeedback/<novelId>/<commentId>', methods=['GET', 'POST'])
@login_required
def deletefeedback(novelId, commentId):
    form = CommentForm()
    comment = Comments.query.filter_by(id = commentId, novel_id = novelId).first()
    if comment.user_id != current_user.id:
        abort(403)
    else:
        if comment != None:
            db.session.delete(comment)
            db.session.commit()

            return redirect(url_for('novels.addfeedback', novelId=novelId))

    return render_template('addfeedback.html', form=form, comments=Comments.query.all(), count=Comments.query.count())


@novels.route('/editfeedback/<novelId>/<commentId>', methods=['GET', 'POST'])
@login_required
def editfeedback(novelId, commentId):
    form = CommentForm()
    comment = Comments.query.filter_by(id = commentId, novel_id = novelId).first()
    if comment.user_id != current_user.id:
        abort(403)
    if form.validate_on_submit():
        comment.feedback = form.feedback.data
        db.session.commit()

        return redirect(url_for('novels.addfeedback', novelId=novelId))

    elif request.method == 'GET':
        form.feedback.data = comment.feedback

    return render_template('addfeedback.html', form=form)


@novels.route('/like/<novelId>/<action>')
@login_required
def likeaction(novelId, action):
    novel = Novel.query.filter_by(id=novelId).first_or_404()
    if action == 'like':
        current_user.like_novel(novel)
        db.session.commit()
    if action == 'unlike':
        current_user.unlike_novel(novel)
        db.session.commit()
    return redirect(request.referrer)