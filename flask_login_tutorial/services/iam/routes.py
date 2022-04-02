"""Routes for user authentication."""
import json

from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_user

from ... import login_manager
from .auth.login import login_local
from .auth.signup import signup as auth_signup
from .forms import LoginForm, SignupForm
from .providers.github import github_oauth
from .providers.google import google_oauth

from .authorize.core import UserManager

github = None
google = None

# Blueprint Configuration
iam_bp = Blueprint(
    "iam_bp", __name__, template_folder="templates", static_folder="static"
)


@iam_bp.before_app_first_request
def register_modules():
    global github
    global google
    github = github_oauth()
    google = google_oauth()


@iam_bp.route("/signup", methods=["GET", "POST"])
def signup():
    """
    User sign-up page.

    GET requests serve sign-up page.
    POST requests validate form & user creation.
    """
    form = SignupForm()
    if form.validate_on_submit():
        username = form.name.data
        email = form.email.data
        password = form.password.data
        msg = auth_signup(username=username, email=email, password=password)
        if not len(msg):
            return redirect(url_for("main_bp.dashboard"))
        flash(msg)
    return render_template(
        "signup.jinja2",
        title="Create an Account.",
        form=form,
        template="signup-page",
        body="Sign up for a user account.",
    )


@iam_bp.route("/login-github")
def login_github():
    redirect_uri = url_for("github_authorized", _external=True)
    return github.authorize_redirect(redirect_uri)


@iam_bp.route("/google-github")
def login_google():
    redirect_uri = url_for("google_authorized", _external=True)
    return google.authorize_redirect(redirect_uri)


@iam_bp.route("/login", methods=["GET", "POST"])
def login():
    """
    Log-in page for registered users.

    GET requests serve Log-in page.
    POST requests validate and redirect user to dashboard.
    """

    # Bypass if user is logged in
    if current_user.is_authenticated:
        print(current_user.__dict__)
        UserManager().disable_user()
        return redirect(url_for("main_bp.dashboard"))

    form = LoginForm()
    # Validate login attempt
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        err = login_local(email, password)
        if len(err):
            flash(err)
            return redirect(url_for("iam_bp.login"))
        print(current_user.is_authenticated)
        next_page = request.args.get("next")
        return redirect(next_page or url_for("main_bp.dashboard"))

    return render_template(
        "login.jinja2",
        form=form,
        title="Log in.",
        template="login-page",
        body="Log in with your User account.",
    )


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash("You must be logged in to view that page.")
    return redirect(url_for("iam_bp.login"))
