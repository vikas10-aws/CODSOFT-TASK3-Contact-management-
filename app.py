from flask import Flask, render_template, request, redirect, url_for, flash, session
import csv
import os
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Paths to the CSV files
contacts_csv_file = 'contacts.csv'

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

# Login required decorator (No need for user credentials now, just check if session exists)
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

# User Logout (No longer needed for registration/login)
@app.route('/logout')
@login_required
def logout():
    session.pop('username', None)
    flash('You have successfully logged out.')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
