// calculator.js
document.addEventListener('DOMContentLoaded', function() {
    const incomeInput = document.getElementById('incomeInput');
    const payoutDisplay = document.getElementById('payoutDisplay');
    const typeLabel = document.getElementById('typeLabel');

    if (incomeInput) {
        incomeInput.addEventListener('input', function(e) {
            let income = parseFloat(e.target.value) || 0;
            let payout = 0;
            let type = "";

            // 1. Claim ประเภทผู้มีรายได้น้อย (< 6500 บาท)
            if (income < 6500) {
                payout = 6500;
                type = "TYPE: LOW_INCOME";
            } 
            // 2. Claim ประเภทผู้มีรายได้สูง (>= 50000 บาท)
            else if (income >= 50000) {
                payout = Math.min(income / 5, 20000); 
                type = "TYPE: HIGH_INCOME";
            } 
            // 3. Claim ประเภททั่วไป (6500 - 50000 บาท)
            else {
                payout = Math.min(income, 20000);
                type = "TYPE: GENERAL";
            }

            // แสดงผลลัพธ์บนหน้า View 
            payoutDisplay.innerText = payout.toLocaleString(undefined, {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            });
            typeLabel.innerText = type;
        });
    }
});