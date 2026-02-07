from flask import Flask, render_template, request, redirect, session, url_for
import json
import os
import hashlib
from controller.submitcal import submit_bp 

app = Flask(__name__)
app.secret_key = 'ImTooLazyToMakethisENVFile!!!'

# ลงทะเบียน Controller
app.register_blueprint(submit_bp)

# กำหนด Path ไฟล์
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'data', 'database.json')
USER_DB_PATH = os.path.join(BASE_DIR, 'data', 'users.json')

# ฟังก์ชันโหลด User จากไฟล์ JSON
def load_users():
    if not os.path.exists(USER_DB_PATH):
        return {}
    with open(USER_DB_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password_input = request.form.get('password')
        
        # 1. กรณีประชาชน (ไม่ต้องใช้รหัสผ่าน)
        if username == 'citizen':
            session['logged_in'] = True
            session['role'] = 'citizen'
            session['user'] = 'CITIZEN'
            return redirect('/submit')

        # 2. กรณีเจ้าหน้าที่/Admin (ตรวจสอบ Hash)
        users_db = load_users()
        hashed_input = hashlib.sha256(password_input.encode()).hexdigest()
        
        if username in users_db and users_db[username] == hashed_input:
            session['logged_in'] = True
            session['role'] = 'officer' # เจ้าหน้าที่
            session['user'] = username
            return redirect('/')
        else:
            return render_template('login.html', error="ACCESS DENIED // Invalid Credentials")
            
    return render_template('login.html')

# Guest Login 
@app.route('/login_guest')
def login_guest():
    session['logged_in'] = True
    session['role'] = 'guest'
    session['user'] = 'GUEST_VIEWER'
    return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

# Dashboard
@app.route('/')
def index():
    if not session.get('logged_in'):
        return redirect('/login')
    
    # Citizen ห้ามเข้า Dashboard
    if session.get('role') == 'citizen':
        return redirect('/submit')

    #  ประกาศตัวแปรเริ่มต้นก่อน เพื่อป้องกัน UnboundLocalError
    claims = []
    compensations = []
    claimants = []
    
    if os.path.exists(DB_PATH):
        with open(DB_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # ดึงข้อมูลใส่ตัวแปรที่ประกาศไว้
            claims = data.get('claims', [])
            compensations = data.get('compensations', [])
            claimants = data.get('claimants', [])

    # ส่งตัวแปรที่เตรียมไว้เข้า template 
    return render_template('dashboard.html', 
                           claims=claims, 
                           compensations=compensations, 
                           claimants=claimants,
                           user=session.get('user', 'UNKNOWN'),
                           role=session.get('role'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)