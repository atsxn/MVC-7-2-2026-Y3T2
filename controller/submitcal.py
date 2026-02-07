# controller/submitcal.py

from flask import Blueprint, request, redirect, flash, session, render_template
import json
import os
import random
import datetime
from models.claim_models import Claim, LowIncomeClaim, HighIncomeClaim

submit_bp = Blueprint('submit', __name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'data', 'database.json')

def load_db():
    if not os.path.exists(DB_PATH): return None
    with open(DB_PATH, 'r', encoding='utf-8') as f: return json.load(f)

def save_db(data):
    with open(DB_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

@submit_bp.route('/submit', methods=['GET'])
def show_submit_page():
    # อนุญาตให้ทุกคนที่ Login แล้วเข้าได้ (รวมถึง Guest)
    if not session.get('logged_in'):
        return redirect('/login')
    return render_template('submit.html')

@submit_bp.route('/calculate', methods=['POST'])
def calculate():
    try:
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        income_str = request.form.get('income')

        if not first_name or not last_name or not income_str:
            raise ValueError("กรุณากรอกข้อมูลให้ครบถ้วน")

        income = float(str(income_str).replace(',', ''))

        # ถ้าเป็น Officer (Admin) ให้เติมคำว่า [TEST] 
        if session.get('role') == 'officer':
            first_name = f"[TEST] {first_name}"


        # เลือก Model
        if income < 6500:
            model = LowIncomeClaim()
            c_type = "Low Income"
        elif income >= 50000:
            model = HighIncomeClaim()
            c_type = "High Income"
        else:
            model = Claim()
            c_type = "General"

        amount = model.calculate(income)

        # เตรียมข้อมูลบันทึก
        db = load_db()
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        claimant_id = str(random.randint(1000, 9999))
        claim_id = str(random.randint(10000000, 99999999))

        new_claimant = {
            "claimant_id": claimant_id,
            "first_name": first_name, # ชื่อนี้จะมี [TEST] ถ้า admin เป็นคนกรอก
            "last_name": last_name,
            "monthly_income": income,
            "type": c_type
        }
        db['claimants'].append(new_claimant)

        new_claim = {
            "claim_id": claim_id,
            "claimant_id": claimant_id,
            "submission_date": current_date,
            "status": "PENDING"
        }
        db['claims'].append(new_claim)

        new_compensation = {
            "claim_id": claim_id,
            "amount": amount,
            "calculation_date": current_date
        }
        db['compensations'].append(new_compensation)
        
        save_db(db)
        flash(f"บันทึกสำเร็จ! รหัสคำขอ #{claim_id}", "success")
        
        # ส่งเสร็จ ถ้าเป็น Admin ให้กลับ Dashboard จะได้เห็นผลเลย
        if session.get('role') == 'officer':
            return redirect('/')
        else:
            return redirect('/submit')

    except Exception as e:
        flash(f"ERROR: {str(e)}", "error")
        return redirect('/submit')

# Approve/Deny Routes 
@submit_bp.route('/approve/<claim_id>', methods=['POST'])
def approve_claim(claim_id):
    if session.get('role') != 'officer': return redirect('/')
    db = load_db()
    for claim in db['claims']:
        if claim['claim_id'] == str(claim_id):
            claim['status'] = "APPROVED"
            break
    save_db(db)
    flash(f"Approved #{claim_id}", "success")
    return redirect('/')

@submit_bp.route('/deny/<claim_id>', methods=['POST'])
def deny_claim(claim_id):
    if session.get('role') != 'officer': return redirect('/')
    db = load_db()
    for claim in db['claims']:
        if claim['claim_id'] == str(claim_id):
            claim['status'] = "DENIED"
            break
    save_db(db)
    flash(f"Denied #{claim_id}", "error")
    return redirect('/')