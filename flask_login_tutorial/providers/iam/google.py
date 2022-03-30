import json
from flask import request, session, redirect, url_for, current_app

from flask_login import login_user
from ... import authlib_oauth_client
from ...models.iam.user import User, db

""" ===== Steps create client id, client secret
1. Access to https://console.cloud.google.com/
2. Create new Project XXX
3. Select Project XXX -> OAuth consent screen: create new
4. Select Project XXX -> Credentials:
    - Click button `CREATE CREDENTIALS` -> OAuth client ID
    - Select Appication type: Web application
"""

settings = {
    'google_oauth_client_id': '799891405851-nja673g09c7c28stpp8n2ilpn653lk5h.apps.googleusercontent.com',
    'google_oauth_client_secret': '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',
    'google_base_url': 'https://openidconnect.googleapis.com/v1/',
    'google_token_url': 'https://oauth2.googleapis.com/token',
    'google_authorize_url': 'https://accounts.google.com/o/oauth2/v2/auth',
    'google_oauth_scope': 'openid email profile'
}


def google_oauth():

    def fetch_google_token():
        return session.get('google_token')

    def update_token(token):
        session['google_token'] = token
        return token

    google = authlib_oauth_client.register(
        'google',
        client_id=settings.get('google_oauth_client_id'),
        client_secret=settings.get('google_oauth_client_secret'),
        api_base_url=settings.get('google_base_url'),
        request_token_url=None,
        access_token_url=settings.get('google_token_url'),
        authorize_url=settings.get('google_authorize_url'),
        client_kwargs={'scope': settings.get('google_oauth_scope')},
        fetch_token=fetch_google_token,
        update_token=update_token)

    @current_app.route('/google/authorized')
    def google_authorized():
        session['google_oauthredir'] = url_for(
            '.google_authorized', _external=True)
        token = google.authorize_access_token()
        if token is None:
            return 'Access denied: reason=%s error=%s' % (
                request.args['error_reason'],
                request.args['error_description']
            )
        session['google_token'] = (token)
        user_data = json.loads(google.get('userinfo').text)
        first_name = user_data['given_name']
        surname = user_data['family_name']
        email = user_data['email']
        
        existing_user = User.query.filter_by(
            email=email, login_type='google').first()
        print(existing_user)
        if existing_user is None:
            user = User(
                name=first_name, email=email, login_type='google')
            db.session.add(user)
            db.session.commit()  # Create new user
            login_user(user)
        else:
            login_user(existing_user)
        return redirect(url_for("main_bp.dashboard"))

    return google
