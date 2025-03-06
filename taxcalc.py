import streamlit as st

def calculate_take_home(gross_salary):
    # Standard Deduction for salaried individuals
    standard_deduction = 75_000
    
    # Employee Provident Fund (EPF) - 6% deducted from employee's salary
    employee_pf = 0.06 * gross_salary
    employer_pf = 0.06 * gross_salary  # Employer contribution (not deducted from salary)

    # Net taxable income after standard deduction and employee PF
    taxable_income = max(0, gross_salary - standard_deduction - employee_pf)
    
    # Revised Tax Slabs for FY 2025-26 (New Regime)
    tax_slabs = [
        (4_00_000, 0.00),  # 0% for ₹0 - ₹4L
        (4_00_000, 0.05),  # 5% for ₹4L - ₹8L
        (4_00_000, 0.10),  # 10% for ₹8L - ₹12L
        (4_00_000, 0.15),  # 15% for ₹12L - ₹16L
        (4_00_000, 0.20),  # 20% for ₹16L - ₹20L
        (4_00_000, 0.25),  # 25% for ₹20L - ₹24L
    ]

    # Remaining income above ₹24L taxed at 30%
    if taxable_income > 24_00_000:
        tax_slabs.append((taxable_income - 24_00_000, 0.30))
    
    # Compute tax
    total_tax = 0
    remaining_income = taxable_income
    
    for slab_amount, rate in tax_slabs:
        if remaining_income > 0:
            taxable_amount = min(slab_amount, remaining_income)
            total_tax += taxable_amount * rate
            remaining_income -= taxable_amount
    
    # Apply rebate u/s 87A only if taxable income is **≤ 12,00,000**, not 12,75,000
    if taxable_income <= 12_00_000:
        total_tax = max(0, total_tax - 60_000)
    
    # Apply surcharge based on income
    if taxable_income > 50_00_000:
        if taxable_income <= 1_00_00_000:
            surcharge = 0.10 * total_tax  # 10% surcharge for ₹50L-₹1Cr
        elif taxable_income <= 2_00_00_000:
            surcharge = 0.15 * total_tax  # 15% surcharge for ₹1Cr-₹2Cr
        elif taxable_income <= 5_00_00_000:
            surcharge = 0.25 * total_tax  # 25% surcharge for ₹2Cr-₹5Cr
        else:
            surcharge = 0.37 * total_tax  # 37% surcharge for ₹5Cr+
        total_tax += surcharge
    
    # Apply 4% Health & Education Cess
    cess = total_tax * 0.04
    total_tax += cess

    # Net annual salary after tax
    net_annual_salary = gross_salary - total_tax - employee_pf  # Deduct employee PF

    # Monthly take-home salary before deductions
    monthly_take_home = net_annual_salary / 12
    
    # Deduct professional tax (₹200 per month)
    professional_tax = 200
    final_monthly_take_home = monthly_take_home - professional_tax

    # Calculate Monthly PF Contribution
    monthly_pf = (employer_pf + employee_pf) / 12
    
    return final_monthly_take_home, monthly_pf, total_tax

# Streamlit UI
st.title("Take-Home Salary Calculator (FY 2025-26)")

gross_salary = st.slider("Select Gross Annual Salary (₹)", min_value=3_00_000, max_value=1_00_00_000, step=50_000, value=15_00_000)

take_home, pf_amount, tax_amount = calculate_take_home(gross_salary)

st.subheader("Results:")
st.write(f"### Monthly Take-Home Salary: ₹{take_home:,.2f}")
st.write(f"### Monthly Provident Fund Contribution (Employer + Employee): ₹{pf_amount:,.2f}")
st.write(f"### Annual Tax Payable: ₹{tax_amount:,.2f}")

