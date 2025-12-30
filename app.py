from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from forms import StudentForm, LoginForm, ContactForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///secure_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'supersecurekey'  # Used for sessions + CSRF protection

# Secure session cookies
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# ----------------- MODELS ------------------
class Student(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(100))
    lname = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(50))
    city = db.Column(db.String(100))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))

# ----------------- ROUTES ------------------

@app.route('/')
def index():
    if 'user' not in session:
        return redirect('/login')
    students = Student.query.all()
    return render_template('index.html', students=students)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session['user'] = user.email
            flash('Login successful!', 'success')
            return redirect('/')
        else:
            flash('Invalid credentials', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Logged out successfully', 'info')
    return redirect('/login')

@app.route('/add', methods=['POST'])
def add():
    form = StudentForm()
    if form.validate_on_submit():
        new_student = Student(
            fname=form.fname.data,
            lname=form.lname.data,
            email=form.email.data,
            phone=form.phone.data,
            city=form.city.data
        )
        db.session.add(new_student)
        db.session.commit()
        flash('Student added successfully', 'success')
    else:
        flash('Invalid input detected!', 'danger')
    return redirect('/')

@app.route('/delete/<int:sno>')
def delete(sno):
    student = Student.query.get_or_404(sno)
    db.session.delete(student)
    db.session.commit()
    flash('Record deleted', 'info')
    return redirect('/')

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    student = Student.query.get_or_404(sno)
    form = StudentForm(obj=student)
    if form.validate_on_submit():
        form.populate_obj(student)
        db.session.commit()
        flash('Record updated successfully', 'success')
        return redirect('/')
    return render_template('update.html', student=student, form=form)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        flash('Message sent successfully!', 'success')
        return redirect('/')
    return render_template('contact.html', form=form)

# ----------------- ERROR HANDLING ------------------
@app.errorhandler(404)
def not_found_error(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Create default admin user
        if not User.query.filter_by(email='admin@example.com').first():
            hashed_pw = bcrypt.generate_password_hash('Admin@123').decode('utf-8')
            db.session.add(User(email='admin@example.com', password=hashed_pw))
            db.session.commit()
    app.run(debug=True)
