from flask import Flask, render_template, request, redirect
import mysql.connector
from config import db_config

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM phones")
    phones = cursor.fetchall()
    conn.close()
    return render_template('index.html', phones=phones)

@app.route('/admin')
def admin():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM phones")
    phones = cursor.fetchall()
    conn.close()
    return render_template('admin.html', phones=phones)

@app.route('/add_phone', methods=['GET', 'POST'])
def add_phone():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        description = request.form['description']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO phones (name, price, description) VALUES (%s, %s, %s)",
                       (name, price, description))
        conn.commit()
        conn.close()
        return redirect('/admin')
    return render_template('add_phone.html')

@app.route('/delete/<int:phone_id>')
def delete_phone(phone_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM phones WHERE id = %s", (phone_id,))
    conn.commit()
    conn.close()
    return redirect('/admin')


if __name__ == '__main__':
    app.run(debug=True)