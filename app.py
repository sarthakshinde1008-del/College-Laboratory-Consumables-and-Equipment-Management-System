from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root123",
        database="college_lab"
    )

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/save', methods=['POST'])
def save():
    name = request.form['name']
    category = request.form['category']
    quantity = request.form['quantity']
    unit = request.form['unit']
    lab = request.form['lab']

    con = connect_db()
    cur = con.cursor()

    sql = """INSERT INTO inventory
             (name, category, quantity, unit, lab)
             VALUES (%s, %s, %s, %s, %s)"""

    cur.execute(sql, (name, category, quantity, unit, lab))
    con.commit()

    cur.close()
    con.close()

    return """
    Item saved successfully!
    <br><a href="/">Go Back</a>
    <br><a href="/show">View Inventory</a>
    """

@app.route('/show')
def show():
    con = connect_db()
    cur = con.cursor()

    cur.execute("SELECT * FROM inventory ORDER BY id DESC")
    data = cur.fetchall()

    cur.close()
    con.close()

    return render_template('show.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)