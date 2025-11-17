# app.py
from flask import Flask, request, jsonify, g, send_from_directory
import sqlite3
import os
import uuid
from datetime import datetime

DB = 'ctf_loans.db'
FLAG = os.environ.get('CTF_FLAG', 'CTF{example_flag_change_me}')
FLAG_HARD = os.environ.get('CTF_FLAG_HARD', 'CTF{hard_stage_flag_example}')
ADMIN_TOKEN = os.environ.get('ADMIN_TOKEN', 'admintoken123')  # seed default

app = Flask(__name__, static_folder='static')
app.config['JSON_SORT_KEYS'] = False

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DB)
        db.row_factory = sqlite3.Row
    return db

def init_db():
    db = get_db()
    db.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY, username TEXT UNIQUE
        )
    ''')
    db.execute('''
        CREATE TABLE IF NOT EXISTS loans (
            id TEXT PRIMARY KEY,
            user_id TEXT,
            amount INTEGER,
            interest_rate REAL,
            approved INTEGER DEFAULT 0,
            created_at TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')
    db.execute('''
        CREATE TABLE IF NOT EXISTS solves (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            flag TEXT,
            stage TEXT,
            ts TEXT
        )
    ''')
    db.commit()

@app.before_first_request
def setup():
    init_db()
    db = get_db()
    cur = db.execute("SELECT * FROM users WHERE username = ?", ('alice',))
    if cur.fetchone() is None:
        uid = str(uuid.uuid4())
        db.execute("INSERT INTO users (id, username) VALUES (?, ?)", (uid, 'alice'))
        db.commit()
    # ensure static backup file exists (simulated accidental leak)
    os.makedirs(app.static_folder, exist_ok=True)
    with open(os.path.join(app.static_folder, 'admin_token.bak'), 'w') as f:
        f.write("# backup file - DO NOT COMMIT\nADMIN_TOKEN=%s\n" % ADMIN_TOKEN)

def get_user_by_name(username):
    db = get_db()
    cur = db.execute("SELECT * FROM users WHERE username = ?", (username,))
    return cur.fetchone()

@app.route('/')
def index():
    return open('client.html', 'r').read()

@app.route('/apply', methods=['POST'])
def apply():
    db = get_db()
    data = request.get_json(force=True)
    username = data.get('username')
    user = get_user_by_name(username)
    if not user:
        return jsonify({'error': 'unknown user'}), 400

    amount = int(data.get('amount', 0))
    interest_rate = float(data.get('interest_rate', 10.0))
    approved = 1 if data.get('approved') in (True, 'true', '1', 1) else 0

    loan_id = str(uuid.uuid4())
    db.execute(
        "INSERT INTO loans (id, user_id, amount, interest_rate, approved, created_at) VALUES (?, ?, ?, ?, ?, ?)",
        (loan_id, user['id'], amount, interest_rate, approved, datetime.utcnow().isoformat())
    )
    db.commit()

    return jsonify({'ok': True, 'loan_id': loan_id})

@app.route('/loans', methods=['GET'])
def loans():
    username = request.args.get('username')
    user = get_user_by_name(username)
    if not user:
        return jsonify({'error': 'unknown user'}), 400
    db = get_db()
    cur = db.execute("SELECT id, amount, interest_rate, approved, created_at FROM loans WHERE user_id = ?", (user['id'],))
    loans = [dict(row) for row in cur.fetchall()]
    return jsonify({'loans': loans})

@app.route('/flag', methods=['GET'])
def flag():
    username = request.args.get('username')
    user = get_user_by_name(username)
    if not user:
        return jsonify({'error': 'unknown user'}), 400
    db = get_db()
    cur = db.execute("SELECT 1 FROM loans WHERE user_id = ? AND approved = 1 LIMIT 1", (user['id'],))
    if cur.fetchone():
        # record solve for basic stage
        db.execute("INSERT INTO solves (username, flag, stage, ts) VALUES (?, ?, ?, ?)",
                   (username, FLAG, 'basic', datetime.utcnow().isoformat()))
        db.commit()
        return jsonify({'flag': FLAG})
    else:
        return jsonify({'error': 'no approved loan found'}), 403

# Admin endpoints
def check_admin_token(token):
    return token == ADMIN_TOKEN

@app.route('/admin')
def admin_panel():
    # serve admin panel (JS will call admin endpoints)
    return open('admin.html', 'r').read()

@app.route('/admin/approve', methods=['POST'])
def admin_approve():
    token = request.headers.get('X-Admin-Token', '')
    if not check_admin_token(token):
        return jsonify({'error': 'forbidden'}), 403
    data = request.get_json(force=True)
    loan_id = data.get('loan_id')
    if not loan_id:
        return jsonify({'error': 'loan_id required'}), 400
    db = get_db()
    cur = db.execute("SELECT * FROM loans WHERE id = ?", (loan_id,))
    row = cur.fetchone()
    if not row:
        return jsonify({'error': 'loan not found'}), 404
    db.execute("UPDATE loans SET approved = 1 WHERE id = ?", (loan_id,))
    db.commit()
    return jsonify({'ok': True, 'loan_id': loan_id})

# Harder stage: only returns hard flag when user has an approved loan AND
# that loan has amount >= 1000000 (one million) AND interest_rate == 0.
@app.route('/hard_flag', methods=['GET'])
def hard_flag():
    username = request.args.get('username')
    user = get_user_by_name(username)
    if not user:
        return jsonify({'error': 'unknown user'}), 400
    db = get_db()
    # strict check: approved and amount >= 1_000_000 and zero interest
    cur = db.execute("SELECT * FROM loans WHERE user_id = ? AND approved = 1 AND amount >= ? AND interest_rate = ? LIMIT 1",
                     (user['id'], 1000000, 0.0))
    row = cur.fetchone()
    if row:
        db.execute("INSERT INTO solves (username, flag, stage, ts) VALUES (?, ?, ?, ?)",
                   (username, FLAG_HARD, 'hard', datetime.utcnow().isoformat()))
        db.commit()
        return jsonify({'flag': FLAG_HARD})
    else:
        return jsonify({'error': 'conditions not met for hard flag'}), 403

# Simulated leak - static backup file route (served from static folder)
@app.route('/backup/<path:filename>')
def backup_files(filename):
    return send_from_directory(app.static_folder, filename)

# Grader: simple API that returns solves (for local scoreboard preview)
@app.route('/_solves', methods=['GET'])
def list_solves():
    db = get_db()
    cur = db.execute("SELECT username, flag, stage, ts FROM solves ORDER BY ts DESC")
    rows = [dict(row) for row in cur.fetchall()]
    return jsonify({'solves': rows})

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
