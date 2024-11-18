from flask import Flask, render_template, request, redirect, url_for, flash
import csv
import os

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

# Home page: View Contacts
@app.route('/')
def home():
    contacts = load_contacts()  # Load contacts from CSV
    return render_template('home.html', contacts=contacts)

# Add Contact
@app.route('/add', methods=['GET', 'POST'])
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

# Update Contact
@app.route('/update/<int:index>', methods=['GET', 'POST'])
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

# Delete Contact
@app.route('/delete/<int:index>')
def delete_contact(index):
    contacts = load_contacts()  # Load contacts from CSV
    contacts.pop(index)  # Remove the contact
    
    # Save updated contacts to CSV
    save_contacts(contacts)
    
    flash('Contact deleted successfully!')
    return redirect(url_for('home'))

# Search Contact
@app.route('/search', methods=['GET', 'POST'])
def search_contact():
    if request.method == 'POST':
        query = request.form['query'].lower()
        contacts = load_contacts()  # Load contacts from CSV
        results = [contact for contact in contacts if query in contact['name'].lower() or query in contact['phone']]
        return render_template('home.html', contacts=results)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
