from flask import Flask, render_template, request, redirect, url_for
import psycopg2

from flask_sqlalchemy import SQLAlchemy
# Connection with DB
conn = psycopg2.connect(database='flask_db',
                        user='postgres',
                        password='root@1453',
                        host='localhost',
                        port='5432')

# create a cursor
cur = conn.cursor()
cur.execute(
    '''CREATE TABLE IF NOT EXISTS products (id serial \
    PRIMARY KEY, name varchar(100), price float);''')

# Insert some data into the table
cur.execute(
    '''INSERT INTO products (name, price) VALUES \
    ('Apple', 1.99), ('Orange', 0.99), ('Banana', 0.59);''')

# commit the changes
conn.commit()

# close the cursor and connection
cur.close()
conn.close()
app = Flask(__name__)
JOBS = [
    {
        'id': 1,
        'title': 'Data Analyst',
        'location': 'Bengaluru, India',
        'salary': 'Rs. 10,00,000'
    },
    {
        'id': 2,
        'title': 'Data Scientist',
        'location': 'Delhi, India',
        'salary': 'Rs. 15,00,000'
    },
    {
        'id': 3,
        'title': 'Frontend Engineer',
        'location': 'Remote'
    },
    {
        'id': 4,
        'title': 'Backend Engineer',
        'location': 'San Francisco, USA',
        'salary': '$150,000'
    }
]


@app.route('/')
def index():
    conn = psycopg2.connect(database="flask_db",
                            user="postgres",
                            password="root@1453",
                            host="localhost", port="5432")
    cur = conn.cursor()

    # Select all products from the table
    cur.execute('''SELECT * FROM products''')

    # Fetch the data
    data = cur.fetchall()

    # close the cursor and connection
    cur.close()
    conn.close()

    return render_template('index.html', data=data)


@app.route('/create', methods=['POST'])
def create():
    conn = psycopg2.connect(database="flask_db",
                            user="postgres",
                            password="root@1453",
                            host="localhost", port="5432")

    cur = conn.cursor()

    # Get the data from the form
    name = request.form['name']
    price = request.form['price']

    # Insert the data into the table
    cur.execute(
        '''INSERT INTO products \
        (name, price) VALUES (%s, %s)''',
        (name, price))

    # commit the changes
    conn.commit()

    # close the cursor and connection
    cur.close()
    conn.close()

    return redirect(url_for('index'))


@app.route('/update', methods=['POST'])
def update():
    conn = psycopg2.connect(database="flask_db",
                            user="postgres",
                            password="root@1453",
                            host="localhost", port="5432")

    cur = conn.cursor()

    # Get the data from the form
    name = request.form['name']
    price = request.form['price']
    id = request.form['id']

    # Update the data in the table
    cur.execute(
        '''UPDATE products SET name=%s,\
        price=%s WHERE id=%s''', (name, price, id))

    # commit the changes
    conn.commit()
    return redirect(url_for('index'))


@app.route('/delete', methods=['POST'])
def delete():
    conn = psycopg2.connect(database="flask_db", user="postgres",
                            password="root",
                            host="localhost", port="5432")
    cur = conn.cursor()

    # Get the data from the form
    id = request.form['id']

    # Delete the data from the table
    cur.execute('''DELETE FROM products WHERE id=%s''', (id,))

    # commit the changes
    conn.commit()

    # close the cursor and connection
    cur.close()
    conn.close()

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
