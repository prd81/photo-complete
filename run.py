# -*- coding: utf-8 -*-
import os
from flask import Flask, render_template, request, session
from flask_session import Session
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField
import cv2
import json
from converters import uri_to_cv, file_to_uri, cv_to_uri
from inpaint import inpaint

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'hard to guess string'
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'uploads')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_TYPE'] = 'filesystem'

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)  # set maximum file size, default is 16MB

Session(app)


class UploadForm(FlaskForm):
    photo = FileField(validators=[FileAllowed(photos, 'Image only!'), FileRequired('File was empty!')])
    submit = SubmitField('Upload')


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    form = UploadForm()
    if form.validate_on_submit():
        f = form.photo.data
        file_url = file_to_uri(f)
        session['orig'] = file_url
        return render_template('canvas.html', file_url = file_url)
    return render_template('index.html', form=form)


@app.route('/upload', methods = ['POST'])
def upload():
    data = request.form['URI']
    session['mask'] = data
    filename = 'mask.jpeg'
    return json.dumps({'filename': filename})


@app.route('/results', methods = ['GET', 'POST'])
def done():
    orig = session.get('orig')
    mask = session.get('mask')
    rest = cv_to_uri(inpaint(uri_to_cv(orig), uri_to_cv(mask)))
    return render_template('done.html', orig=orig, mask=mask, rest=rest)
