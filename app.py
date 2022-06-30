from flask import *
import datetime
import sqlite3

def read_phonelist(C):
    cur = C.cursor()
    cur.execute("SELECT * FROM phonelist;")
    rows = cur.fetchall()
    cur.close()
    return rows
def read_phone(C, name):
    cur = C.cursor()
    print(f"SELECT phone FROM phonelist WHERE name = '{name}';")
    cur.execute(f"SELECT phone FROM phonelist WHERE name = '{name}';")
    rows = cur.fetchall()
    cur.close()
    return rows
def add_phone(C, name, phone):
    cur = C.cursor()
    cur.execute(f"INSERT INTO phonelist VALUES ('{name}', '{phone}');")
    cur.close()
def delete_phone(C, name):
    cur = C.cursor()
    cur.execute(f"DELETE FROM phonelist WHERE name = '{name}';")
    cur.close()
def save_phonelist(C):
    cur = C.cursor()
    try:
        cur.execute("COMMIT;")
    except:
        print("No changes!")
    cur.close()
def read_name(C, phone):
    cur = C.cursor()
    cur.execute(f"SELECT name FROM phonelist WHERE phone = '{phone}';")
    rows = cur.fetchall()
    cur.close()
    return rows

app = Flask(__name__)

@app.route("/name")
def name_func():
    conn = sqlite3.connect("phone.db")
    rows =read_name(conn)
    return render_template('name.html', list = rows)

@app.route("/phone")
def phone_func():
    return render_template('phone.html')



@app.route("/api")
def api_func():
    conn = sqlite3.connect("phone.db")
    args=request.args
    action = args.get('action', default="Bad action", type=str)
    if action == "Bad action":
        return render_template('api_usage.html', action=action)
    if action == 'phone':
        name = args.get('name', default="No name", type=str)
        if name == "No name":
            return render_template('api_usage.html', action=action)
        phone = read_phone(conn, name)
        if len(phone) < 1:
            return "not found"
        return phone[0][0]
    elif action == 'name':
        phone = args.get('phone', default="No phone", type=str)
        if phone == "No phone":
            return render_template('api_usage.html', action=action)
        name = read_name(conn, phone)
        if len(name) < 1:
            return "not found"

        return name[0][0]
    else:
        return f"Unknown action: '{action}'"

