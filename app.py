from flask import Flask, request, redirect, render_template, url_for
from functools import wraps
import jinja2
import forms
import os
from ghost import Ghost
from flask_oauthlib.client import OAuth

app = Flask(__name__)
app.debug = True
ghost = Ghost()

#decorators
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not ghost.is_signed_in:
            return redirect(url_for('signin', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

#views
@app.route("/", methods=['GET','POST'])
@login_required
def index():

    if request.method == 'POST':
        new_post = ghost.create_post()
        return redirect(url_for('edit', post_id=new_post['id']))

    drafts = ghost.get_drafts()
    return render_template('index.html', posts=drafts['posts'])

@app.route("/edit/<int:post_id>", methods=['GET','POST'])
@login_required
def edit(post_id):

    if request.method == 'POST':
        ghost.save_post(post_id, request.form['title'], request.form['markdown'])

    post = ghost.get_post(post_id)
    return render_template('editor.html', post=post)

@app.route("/signin", methods=['GET', 'POST'])
def signin():

    failed = False
    form = forms.SigninForm(request.form)

    if request.method == 'POST' and form.validate():
        if ghost.signin(form.data['email'], form.data['password']):
            return redirect(url_for('index'))
        else:
            failed = True

    return render_template('signin.html', form=form, failed=failed)

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
