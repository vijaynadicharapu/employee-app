from flask import Flask, render_template, request, redirect
from db import get_connection

app = Flask(__name__)

def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT Exists employees(
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(100),
            department VARCHAR(100)
        )
    """)
    conn.commit()
    cur.close()
    conn.close()
    
init_db()
                          

@app.route("/")
def index():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM employees ORDER BY id")
    employees = cur.fetchall()

    cur.close()
    conn.close()

    return render_template("index.html", employees=employees)

@app.route("/employee", methods=["POST"])
def add_employee():

    name = request.form["name"]
    email = request.form["email"]
    department = request.form["department"]

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO employees(name,email,department)
        VALUES(%s,%s,%s)
        """,
        (name,email,department)
    )

    conn.commit()

    cur.close()
    conn.close()

    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
