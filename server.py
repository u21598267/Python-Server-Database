import os
import sqlite3
from flask import Flask, render_template, request


app = Flask(__name__, static_folder='./static', template_folder='./templates')
connection = sqlite3.connect("Appointments.db")


# Code to delete a record from the database


@app.route('/delete', methods=['POST'])
def delete():
    # Create a connection object
    connection = sqlite3.connect("Appointments.db")

    # From the connection object, create a cursor object
    cursor = connection.cursor()

    # Using the cursor object, call the execute method with select query as the parameter
    cursor.execute("DELETE FROM bookings WHERE id = ?", (request.form['id'],))

    # Commit the changes to the database
    connection.commit()

    # Fetch all rows from the result set
    cursor.execute("SELECT * FROM bookings;")
    rows = cursor.fetchall()

    # Close the connection
    connection.close()

    # Redirect to the home page
    return render_template("index.html", rows=rows)


@app.route('/Add', methods=['POST'])
def Add():
    # Create a connection object
    connection = sqlite3.connect("Appointments.db")
    cursor = connection.cursor()
    file = request.files['image']
    # Add values from form fields to the database
    cursor.execute("INSERT INTO bookings (name, date, time,image) VALUES (?, ?, ?,?)",
                   (request.form['name'], request.form['date'], request.form['time'], file.filename))

    # save request.form['image'] to a file

    folder = 'static'
    if not os.path.exists(folder):
        os.makedirs(folder)

    file.save(os.path.join(folder, file.filename))

    connection.commit()

    # Fetch all rows from the result set
    cursor.execute("SELECT * FROM bookings;")
    rows = cursor.fetchall()

    # Close the connection
    connection.close()

    # Render the HTML template with data from SQLite database
    return render_template("index.html", rows=rows)


@app.route('/')
def index():
    # Create a connection object
    connection = sqlite3.connect("Appointments.db")

    # From the connection object, create a cursor object
    cursor = connection.cursor()

    # Using the cursor object, call the execute method with select query as the parameter
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='bookings';")

    # Fetch all rows from the result set
    rows = cursor.fetchall()

    # Fetch all rows from the result set
    cursor.execute("SELECT * FROM bookings;")
    rows = cursor.fetchall()

    # Close the connection
    connection.close()

    # Render the HTML template with data from SQLite database
    return render_template("index.html", rows=rows)

# This route should be used to update the database


@app.route('/update', methods=['POST'])
def update():
    # Create a connection object
    connection = sqlite3.connect("Appointments.db")

    # From the connection object, create a cursor object
    cursor = connection.cursor()

    # Using the cursor object, call the execute method with select query as the parameter
    cursor.execute("UPDATE bookings SET name = ?, date = ?, time = ? WHERE id = ?",
                   (request.form['name'], request.form['date'], request.form['time'], request.form['id']))

    # Commit the changes to the database
    connection.commit()

    # Fetch all rows from the result set
    cursor.execute("SELECT * FROM bookings;")
    rows = cursor.fetchall()

    # Close the connection
    connection.close()

    # Redirect to the home page
    return render_template("index.html", rows=rows)

# This route should be used to search the data from the database


@app.route('/search', methods=['POST'])
def search():
    # Create a connection object
    connection = sqlite3.connect("Appointments.db")

    # From the connection object, create a cursor object
    cursor = connection.cursor()

    # Using the cursor object, call the execute method with select query as the parameter
    cursor.execute("SELECT * FROM bookings WHERE id = ?",
                   (request.form['id'],))

    # Fetch all rows from the result set
    rows = cursor.fetchall()

    # Close the connection
    connection.close()

    # Render the HTML template with data from SQLite database
    return render_template("index.html", rows=rows)


if __name__ == '__main__':
    app.run(debug=True)
