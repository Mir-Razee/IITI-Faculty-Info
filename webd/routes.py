from webd import app
from flask import redirect, url_for, session, render_template
from webd import oauth

@app.route("/")
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    google = oauth.create_client('google')
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/authorize')
def authorize():
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    resp = google.get('userinfo')
    user_info = resp.json()
    user = oauth.google.userinfo()
    session['profile'] = user_info
    session.permanent = True
    return redirect('/form')

@app.route('/form')
def form():
    user=dict(session).get('profile',None);
    if user:
        return render_template('form.html')
    else:
        return "Please Login as admin"

@app.route('/logout')
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect('/')
