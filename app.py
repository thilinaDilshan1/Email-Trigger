from flask import Flask,request,redirect,render_template,url_for,flash
import mysql.connector
import firebase_admin
from firebase_admin import credentials,firestore

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for flashing messages

cred = credentials.Certificate('email-trigger-firebase-firebase-adminsdk-pau9i-290f874908.json')
firebase_admin.initialize_app(cred)
db = firestore.client()


@app.route('/')
def register():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def get_register():
    email = request.form.get("email")
    name = request.form.get("name")
    password = request.form.get("password")
    
    # Insert data into the firebase
    doc_ref = db.collection('users').document(email)
    doc_ref.set({
        'name': name,
        'email': email,
        'password':  password
    })


    # Return the data in the response to display on the web page
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

         # Check if the user exists and the password matches
        doc_ref = db.collection('users').document(email)
        doc = doc_ref.get()
        if doc.exists and doc.to_dict()['password'] == password:
            return redirect(url_for('welcome', name=doc.to_dict()['name'], email=email))
        else:
            flash('Invalid email or password. Please try again.')
            return redirect(url_for('login'))
    return render_template('login.html')



@app.route('/welcome')
def welcome():
    name = request.args.get('name')
    email = request.args.get('email')
    return render_template('welcome.html', name=name, email=email)


if __name__ == '__main__':
    app.run(debug=True)
