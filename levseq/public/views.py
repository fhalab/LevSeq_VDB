# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import login_required, login_user, logout_user, current_user

from evseql.extensions import login_manager
from evseql.public.forms import LoginForm
from evseql.user.forms import RegisterForm
from evseql.user.models import User
from evseql.utils import flash_errors
import pandas as pd
import json

blueprint = Blueprint("public", __name__, static_folder="../static")


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    return User.get_by_id(int(user_id))


@blueprint.route("/", methods=["GET", "POST"])
def home():
    """Home page."""
    form = LoginForm(request.form)
    data = False
    # Handle logging in
    if request.method == "POST":
        if form.validate_on_submit():
            login_user(form.user)
            flash("You are logged in.", "success")
            redirect_url = request.args.get("next") or url_for("user.experiments")
            # Set the user cookie id
            response = redirect(redirect_url)
            return response
        else:
            flash('Invalid username or password', 'error')

    return render_template("public/home.html", form=form)


@blueprint.route("/logout/")
@login_required
def logout():
    """Logout."""
    logout_user()
    flash("You are logged out.", "info")
    return redirect(url_for("public.home"))


@blueprint.route("/register/", methods=["GET", "POST"])
def register():
    """Register new user."""
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        User.create(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            active=True,
        )
        flash("Thank you for registering. You can now log in.", "success")
        return redirect(url_for("user.experiments"))
    else:
        flash_errors(form)
    return render_template("public/register.html", form=form)


@blueprint.route("/about/")
def about():
    """About page."""
    form = LoginForm(request.form)
    return render_template("public/about.html", form=form)


@blueprint.route('/vis/', methods=['GET', 'POST'])
def vis():
    """Upload the user data."""
    if request.method == 'POST':
        # Check if the post request has the files part
        if 'csv_file' not in request.files:
            return 'using default files'
        csv_file = request.files['csv_file']

        # Process CSV file
        df = pd.read_csv(csv_file)
        df['group'] = [str(w[0]) for w in df['Well'].values]
        df['variable'] = [str(w[1:]) for w in df['Well'].values]

        rows = df.values
        rows = [list(r) for r in rows]
        columns = [{'title': c} for c in df.columns]
        df_for_d3 = df.to_dict(orient='records')  # Each row becomes a dictionary
        numerical_df = df.select_dtypes(include=['number'])
        numerical_columns = [{'title': col} for col in numerical_df.columns]

        return render_template('public/heatmap.html',
                               data=json.dumps({'columns': columns, 'rows': rows}),
                               columns=numerical_columns,
                               df=json.dumps(df_for_d3)
                               )
    else:
        return render_template("public/heatmap.html")

