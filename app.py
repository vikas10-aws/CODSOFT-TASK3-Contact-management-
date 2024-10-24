from flask import Flask, render_template, request, redirect, url_for, flash, session
import csv
import os
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Paths to the CSV files
contacts_csv_file = 'contacts.csv'
users_csv_file = 'users.csv'

# Load contacts from CSV file into memory
def load_contacts():
    contacts = []
    if os.path.exists(contacts_csv_file):
        with open(contacts_csv_file, mode='r') as file:
            reader = csv.DictReader(file)
            contacts = list(reader)
    return contacts

# Save the current list of contacts back to the CSV file
def save_contacts(contacts):
    with open(contacts_csv_file, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['name', 'phone', 'email', 'address'])
        writer.writeheader()  # Write the CSV header
        writer.writerows(contacts)  # Write all contacts

# Load users from CSV file
def load_users():
    users = []
    if os.path.exists(users_csv_file):
        with open(users_csv_file, mode='r') as file:
            reader = csv.DictReader(file)
            users = list(reader)
    return users

# Save new user to CSV file
def save_user(user):
    with open(users_csv_file, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['username', 'password'])
        writer.writerow(user)

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash("Please log in first.")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Home page: View Contacts (requires login)
@app.route('/')
@login_required
def home():
    contacts = load_contacts()  # Load contacts from CSV
    return render_template('home.html', contacts=contacts)

# Add Contact (requires login)
@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_contact():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        address = request.form['address']
        
        # Load contacts and append the new contact
        contacts = load_contacts()
        contacts.append({'name': name, 'phone': phone, 'email': email, 'address': address})
        
        # Save updated contacts to CSV
        save_contacts(contacts)
        
        flash('Contact added successfully!')
        return redirect(url_for('home'))
    return render_template('add_contact.html')

# Update Contact (requires login)
@app.route('/update/<int:index>', methods=['GET', 'POST'])
@login_required
def update_contact(index):
    contacts = load_contacts()  # Load contacts from CSV
    if request.method == 'POST':
        contacts[index]['name'] = request.form['name']
        contacts[index]['phone'] = request.form['phone']
        contacts[index]['email'] = request.form['email']
        contacts[index]['address'] = request.form['address']
        
        # Save updated contacts to CSV
        save_contacts(contacts)
        
        flash('Contact updated successfully!')
        return redirect(url_for('home'))
    return render_template('update_contact.html', contact=contacts[index], index=index)

# Delete Contact (requires login)
@app.route('/delete/<int:index>')
@login_required
def delete_contact(index):
    contacts = load_contacts()  # Load contacts from CSV
    contacts.pop(index)  # Remove the contact
    
    # Save updated contacts to CSV
    save_contacts(contacts)
    
    flash('Contact deleted successfully!')
    return redirect(url_for('home'))

# Search Contact (requires login)
@app.route('/search', methods=['GET', 'POST'])
@login_required
def search_contact():
    if request.method == 'POST':
        query = request.form['query'].lower()
        contacts = load_contacts()  # Load contacts from CSV
        results = [contact for contact in contacts if query in contact['name'].lower() or query in contact['phone']]
        return render_template('home.html', contacts=results)
    return redirect(url_for('home'))

# User Registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if the username already exists
        users = load_users()
        if any(user['username'] == username for user in users):
            flash('Username already exists. Please choose a different one.')
            return redirect(url_for('register'))
        
        # Save the new user to the CSV
        save_user({'username': username, 'password': password})
        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))
    
    return render_template('register.html')

# User Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        users = load_users()
        user = next((user for user in users if user['username'] == username and user['password'] == password), None)
        
        if user:
            session['username'] = username
            flash('Login successful!')
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials. Please try again.')
            return redirect(url_for('login'))
    
    return render_template('login.html')

# User Logout
@app.route('/logout')
@login_required
def logout():
    session.pop('username', None)
    flash('You have successfully logged out.')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
