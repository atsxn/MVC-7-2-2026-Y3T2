import json
import os

# กำหนดเส้นทางไฟล์
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
DB_PATH = os.path.join(DATA_DIR, 'database.json')

def setup_database():
    # 1. สร้างโฟลเดอร์ data ถ้ายังไม่มี
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        print(f"✅ Created directory: {DATA_DIR}")

    # 2. กำหนดโครงสร้างฐานข้อมูล
    db_structure = {
        "claimants": [],      # ตารางผู้ขอเยียวยา
        "claims": [],         # ตารางคำขอ
        "compensations": [],  # ตารางผลการจ่ายเงิน
        "policies": [         # ตารางนโยบาย (มีข้อมูลเริ่มต้น)
            {
                "policy_id": "P01",
                "desc": "นโยบายเยียวยาฉุกเฉิน (Emergency Aid 2026)",
                "max_cap": 20000,
                "condition": "tiered_income"
            }
        ]
    }

    # 3. บันทึกลงไฟล์ .json
    try:
        with open(DB_PATH, 'w', encoding='utf-8') as f:
            json.dump(db_structure, f, indent=4, ensure_ascii=False)
        print(f"Make DB at: {DB_PATH}")

    except Exception as e:
        print(f"Error creating database: {e}")

if __name__ == "__main__":
    setup_database()