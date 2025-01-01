from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from db import init_db,create_user, get_user_by_userid, update_password

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

reset_session = {}


# Initialize the database
init_db()

# User model
class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id

@login_manager.user_loader
def load_user(user_id):
    user_data = get_user_by_userid(user_id)
    return User(user_data['user']) if user_data else None

@app.before_request
def redirect_authenticated_user():
    """Redirect authenticated users to their protected page."""
    if current_user.is_authenticated and request.endpoint in ['login', 'signup']:
        return redirect(url_for('protected', username=current_user.id))

@app.route('/')
def home():
    """Home route redirects to login or protected page based on authentication."""
    return redirect(url_for('login') if not current_user.is_authenticated else url_for('protected', username=current_user.id))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    session.clear()  # Clear previous session data
    if request.method == 'POST':
        user = request.form['user']
        password = request.form['password']

        user_data = get_user_by_userid(user)
        if user_data and check_password_hash(user_data['password'], password):
            session['user'] = user
            session.permanent = True
            return ("Successfully logged")

        flash("Invalid credentials")
    return render_template('login_signup.html', mode="login")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Handle user registration."""
    if request.method == 'POST':
        user = request.form['user']
        password = request.form['password']

        if get_user_by_userid(user):
            flash("User already exists")
        else:
            create_user(user, generate_password_hash(password, method='pbkdf2:sha256'))
            flash("Signup successful. Please log in.")
            return redirect(url_for('login'))

    return render_template('login_signup.html', mode="signup")

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    email_form = True

    if request.method == 'POST':
        username = request.form.get('username')
        new_password = request.form.get('new_password')

        if username and not new_password:
            check_user = get_user_by_userid(username)
            if check_user is None:
                return "User does not exist!"
            
            reset_session['user'] = username
            email_form = False
            return render_template('forgot_password.html', email_form=email_form)

        if reset_session['user'] and new_password:
            hashed_password = generate_password_hash(new_password, method='pbkdf2:sha256')
            update_password(reset_session['user'], hashed_password)
            flash("Password updated successfully!")
            reset_session.clear()
            return redirect("/login")
        
        flash("Some Error Occured!")
        return redirect("/forgot-password")

    return render_template('forgot_password.html', email_form=email_form)

if __name__ == "__main__":
    app.run(debug=True)
