from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)  # Create the Flask app only once
app.secret_key = '40462a98c73b05b994c36d927c25928d' 

# Define correct answers (in a real application, you might pull this from a database)
correct_answers = {
    'question1': 'Paris',
    # Add other questions and their correct answers here
}
leaderboard_data = [
    {'rank': 1, 'username': 'User1', 'points': 1500},
    {'rank': 2, 'username': 'User2', 'points': 1400},
    {'rank': 3, 'username': 'User3', 'points': 1300},
    # Add more entries as needed
]

# Sample rewards data (this would typically come from a database)
rewards_data = [
    {'id': 1, 'title': 'Bonus Spin', 
     'description': 'Get a bonus spin on the wheel today!'},
    {'id': 2, 'title': 'Extra Points', 
     'description': 'Earn extra points for daily login.'},
    {'id': 3, 'title': 'Cashback Offer', 
     'description': 'Receive a special cashback offer when you complete surveys.'},
    # Add more entries as needed
]
# Configuring the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# User model
class User(db.Model):
        __tablename__ = 'user1'
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(150), nullable=False)
        email = db.Column(db.String(150), unique=True, nullable=False)
        phone = db.Column(db.String(15), nullable=False)
        password = db.Column(db.String(200), nullable=False)

        def __init__(self, name, email, phone, password):
            self.name = name
            self.email = email
            self.phone = phone
            self.password = password

@app.route('/signup', methods=['GET', 'POST'])
def signup():
        if request.method == 'POST':
            name = request.form['name']
            email = request.form['email']
            phone = request.form['phone']
            password = request.form['password']
            confirm_password = request.form['confirm_password']

            if password != confirm_password:
                flash('Passwords do not match!', 'danger')
                return redirect('/signup')
            
            new_user = User(
                name=name, 
                email=email, 
                phone=phone, 
                password=generate_password_hash(password)
            )
            db.session.add(new_user)
            try:
                db.session.commit()
                flash('You have successfully signed up!', 'success')
                return redirect(url_for('progress'))
            except Exception as e:
                db.session.rollback()
                flash(f'Error occurred: {e}', 'danger')

        return render_template('signup.html')

    
@app.teardown_appcontext
def initialize_db(exception=None):
    try:
        db.create_all()  # Ensure database and tables are created before running the server
        print("Database initialized successfully.")
    except Exception as e:
        print(f"Error initializing database: {e}")

# Route for login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        # Check if user exists and password is correct
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
        else:
            return "Invalid credentials!", 400

    return render_template('login.html')

# Route for dashboard
@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        return render_template('dashboard.html', user=user)
    return redirect(url_for('login'))


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/leaderboard')
def leaderboard():
    return render_template('leaderboard.html', leaderboard=leaderboard_data) 

@app.route('/spin-the-wheel')
def spin_the_wheel():
    return render_template('spin-the-wheel.html')

@app.route('/trivia')
def trivia():
    return render_template('trivia.html')

@app.route('/submit-trivia', methods=['POST'])
def submit_trivia():
    user_answers = {
        'question1': request.form.get('question1'),
        # Collect other answers here
    }

    score = 0
    for question, answer in user_answers.items():
        if answer == correct_answers.get(question):
            score += 1

    # Optionally flash a message or handle results
    flash(f'Your score: {score}/{len(correct_answers)}', 'success')

    # Redirect to a results page or back to trivia with a message
    return redirect(url_for('trivia'))

@app.route('/surveys')
def surveys():
    return render_template('surveys.html')

@app.route('/submit-survey', methods=['POST'])
def submit_survey():
    # Process survey form data
    satisfaction = request.form.get('satisfaction')
    features = request.form.get('features')
    # Implement your logic for handling survey responses
    # Optionally, store responses in a database or perform other actions
    flash('Thank you for participating in our survey!', 'success')
    return redirect(url_for('surveys'))

# Route for the Daily Rewards page
@app.route('/daily-rewards')
def daily_rewards():
    return render_template('daily-rewards.html', rewards=rewards_data)

# Route for the Scratch Cards page
@app.route('/scratch-cards')
def scratch_cards():
    return render_template('scratch-cards.html')

# Route for the Mini Games page
@app.route('/mini-games')
def mini_games():
    return render_template('mini-games.html')

# Route for the Referral Program page
@app.route('/referral-program')
def referral_program():
    return render_template('referral-program.html')

# Route for the Profile page
@app.route('/profile')
def profile():
    return render_template('profile.html')

# Route for the Help page
@app.route('/help')
def help_page():
    return render_template('help.html')

# Route for the Contact Us page
@app.route('/contact')
def contact():
    return render_template('contact.html')

# Route for the FAQ page
@app.route('/faq')
def faq():
    return render_template('faq.html')

# Route for the Terms of Service page
@app.route('/terms')
def terms():
    return render_template('terms.html')

# Route for the Privacy Policy page
@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

# Route to handle contact form submission (example)

@app.route('/progress')
def progress():
    return render_template('progress.html')

@app.route('/submit-contact', methods=['POST'])
def submit_contact():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')
    # Implement your logic to process the contact form data
    # Redirect to a thank-you or confirmation page
    return redirect(url_for('contact'))  # Redirect to the contact page or a thank-you page

@app.route('/view_data')
def view_data():
    users = User.query.all()
    return render_template('view_data.html', users=users)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  
    app.run(host='0.0.0.0', port=5000)