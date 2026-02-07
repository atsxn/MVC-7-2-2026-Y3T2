
# models/claim_models.py

class Claim: # ประเภททั่วไป
    def calculate(self, income):
        # รายได้ 6,500 - 50,000 ได้ตามรายได้แต่ไม่เกิน 20,000 
        return min(income, 20000)

class LowIncomeClaim: # ผู้มีรายได้น้อย T_T
    def calculate(self, income):
        # รายได้ < 6,500 ได้ 6,500
        return 6500

class HighIncomeClaim: # ผู้มีรายได้สูง
    def calculate(self, income):
        # รายได้ >= 50,000 ได้รายได้/5 แต่ไม่เกิน 20,000 
        return min(income / 5, 20000)