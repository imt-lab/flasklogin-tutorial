"""Logged-in page routes."""
from flask import Blueprint, redirect, render_template, url_for, session
from flask_login import current_user, login_required, logout_user

# Blueprint Configuration
main_bp = Blueprint(
    "main_bp", __name__, template_folder="templates", static_folder="static"
)


@main_bp.route("/", methods=["GET"])
@login_required
def dashboard():
    """Logged-in User Dashboard."""

    session['redis_test'] = 'This is a session variable.'

    return render_template(
        "dashboard.jinja2",
        title="Flask-Login Tutorial.",
        template="dashboard-template",
        current_user=current_user,
        body="You are now logged in!",
    )


@main_bp.route("/logout")
@login_required
def logout():
    """User log-out logic."""
    logout_user()
    return redirect(url_for("auth_bp.login"))


@main_bp.route('/session', methods=['GET'])
@login_required
def session_view():
    """Display session variable value."""
    return render_template(
        'session.jinja2',
        title='Flask-Session Tutorial.',
        template='dashboard-template',
        session_variable=str(session['redis_test'])
    )
