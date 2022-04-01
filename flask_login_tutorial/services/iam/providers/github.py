import json
from flask import request, session, redirect, url_for, current_app
from flask_login import login_user
from .... import authlib_oauth_client
from ..models.user import User, db

settings = {
    'github_oauth_key': 'fca39987737923359b63',
    'github_oauth_secret': '9b87977bf3e3052eba3a4bfc4aa4f588523051d1',
    'github_oauth_scope': 'user:email',
    'github_oauth_api_url': 'https://api.github.com/',
    'github_oauth_token_url': 'https://github.com/login/oauth/access_token',
    'github_oauth_authorize_url': 'https://github.com/login/oauth/authorize',
}


def github_oauth():

    def fetch_github_token():
        return session.get('github_token')

    def update_token(token):
        session['github_token'] = token
        return token

    github = authlib_oauth_client.register(
        'github',
        client_id=settings.get('github_oauth_key'),
        client_secret=settings.get('github_oauth_secret'),
        request_token_params={'scope': settings.get('github_oauth_scope')},
        api_base_url=settings.get('github_oauth_api_url'),
        request_token_url=None,
        access_token_url=settings.get('github_oauth_token_url'),
        authorize_url=settings.get('github_oauth_authorize_url'),
        client_kwargs={'scope': settings.get('github_oauth_scope')},
        fetch_token=fetch_github_token,
        update_token=update_token)

    @current_app.route('/github/authorized')
    def github_authorized():
        session['github_oauthredir'] = url_for('.github_authorized',
                                               _external=True)
        token = github.authorize_access_token()
        if token is None:
            return 'Access denied: reason=%s error=%s' % (
                request.args['error'], request.args['error_description'])
        session['github_token'] = (token)

        # print(session)
        me = json.loads(github.get('user').text)
        # print(me)
        github_username = me['login']
        github_email = me['email']
        print(github_email)

        existing_user = User.query.filter_by(
            email=github_email, login_type='github').first()
        print(existing_user)
        if existing_user is None:
            user = User(
                name=github_username, email=github_email, login_type='github')
            db.session.add(user)
            db.session.commit()  # Create new user
            login_user(user)
        else:
            login_user(existing_user)
        return redirect(url_for("main_bp.dashboard"))

    return github
