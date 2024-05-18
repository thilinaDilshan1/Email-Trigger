from flask import Flask,request,redirect,render_template,url_for,flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for flashing messages


def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',
        port=3308,
        user='root',
        password='',
        database='flask_db'
    )
    return connection

@app.route('/')
def register():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def get_register():
    email = request.form.get("email")
    name = request.form.get("name")
    password = request.form.get("password")
    
    # Insert data into the database
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, password))
    connection.commit()
    cursor.close()
    connection.close()

    # Return the data in the response to display on the web page
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        connection.close()

        if user and user[3] == password:  # Check password
            return redirect(url_for('welcome', name=user[1], email=email))
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
