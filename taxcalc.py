import streamlit as st

def format_currency(amount):
    """
    Formats an integer amount in Indian Rupees format.
    """
    amount = int(round(amount))  # Convert to integer and round off
    amount = str(amount)
    if len(amount) <= 3:
        return f"₹{amount}"

    last_three = amount[-3:]
    remaining = amount[:-3]

    if not remaining:
        return f"₹{last_three}"

    groups = []
    while remaining:
        groups.append(remaining[-2:])
        remaining = remaining[:-2]

    formatted = ",".join(reversed(groups))

    if formatted:
        formatted = formatted + "," + last_three
    else:
        formatted = last_three

    return f"₹{formatted}"

def calculate_take_home(base_salary, bonus_percentage):
    # Standard Deduction for salaried individuals
    standard_deduction = 75_000
    
    # Employee Provident Fund (EPF) - 6% deducted from employee's salary
    employee_pf = 0.06 * base_salary
    employer_pf = 0.06 * base_salary  # Employer contribution (not deducted from salary)

    # Calculate Annual Bonus
    annual_bonus = (bonus_percentage / 100) * base_salary
    
    # Total taxable income including bonus
    taxable_income = max(0, base_salary + annual_bonus - standard_deduction - employee_pf)
    
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
    
    # Compute total tax
    total_tax = 0
    remaining_income = taxable_income
    
    for slab_amount, rate in tax_slabs:
        if remaining_income > 0:
            taxable_amount = min(slab_amount, remaining_income)
            total_tax += taxable_amount * rate
            remaining_income -= taxable_amount
    
    # Apply rebate u/s 87A only if taxable income is **≤ 12,00,000**
    if taxable_income <= 12_00_000:
        total_tax = max(0, total_tax - 60_000)
    
    # Apply surcharge based on total taxable income
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
    net_annual_salary = base_salary - (total_tax * (base_salary / taxable_income)) - employee_pf if taxable_income > 0 else base_salary - employee_pf  
    
    # Monthly take-home salary before deductions
    monthly_take_home = net_annual_salary / 12
    
    # Deduct professional tax (₹200 per month)
    professional_tax = 200
    final_monthly_take_home = monthly_take_home - professional_tax

    # Calculate Monthly PF Contribution
    monthly_pf = (employer_pf + employee_pf) / 12
    
    # Annual Bonus Take-Home (Tax is applied proportionally)
    annual_bonus_take_home = annual_bonus - (total_tax * (annual_bonus / taxable_income)) if taxable_income > 0 else annual_bonus
    
    total_ctc = base_salary + annual_bonus + employer_pf
    
    return final_monthly_take_home, monthly_pf, total_tax, annual_bonus, annual_bonus_take_home, employer_pf, total_ctc

# Streamlit UI
st.title("Take-Home Salary Calculator (FY 2025-26)")

base_salary = st.slider("Select Base Annual Salary (₹)", min_value=3_00_000, max_value=1_00_00_000, step=50_000, value=15_00_000)
bonus_percentage = st.slider("Select Bonus Percentage (%)", min_value=0, max_value=50, step=1, value=16)

take_home, pf_amount, tax_amount, annual_bonus, annual_bonus_take_home, employer_pf, total_ctc = calculate_take_home(base_salary, bonus_percentage)

# Display results in a formatted table
st.subheader("Results")
st.markdown(f"""
    <style>
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        th, td {{
            padding: 10px;
            text-align: left;
        }}
        th {{
            background-color: #f2f2f2;
            font-weight: bold;
        }}
        .highlight-green {{
            font-weight: bold;
            color: green;
        }}
        .highlight-brown {{
            font-weight: bold;
            color: brown;
        }}
        .highlight-red {{
            font-weight: bold;
            color: red;
        }}
        .highlight-purple {{
            font-weight: bold;
            color: purple;
        }}
    </style>
    <table>
        <tr><th>Component</th><th>Amount</th></tr>
        <tr><td>Base Annual Salary</td><td>{format_currency(base_salary)}</td></tr>
        <tr><td>Annual Bonus ({bonus_percentage}%)</td><td>{format_currency(annual_bonus)}</td></tr>
        <tr><td>PF Retirals (Employer) - 6% of Base</td><td>{format_currency(employer_pf)}</td></tr>
        <tr class='highlight-green'><td>Total CTC (Base Annual Salary + Annual Bonus + PF Retirals)</td><td>{format_currency(total_ctc)}</td></tr>
        <tr><td>Annual Tax Payable</td><td>{format_currency(tax_amount)}</td></tr>
        <tr class='highlight-brown'><td>Annual Bonus (Take Home)</td><td>{format_currency(annual_bonus_take_home)}</td></tr>
        <tr class='highlight-purple'><td>Monthly PF Contribution (Employee + Employer)</td><td>{format_currency(pf_amount)}</td></tr>
        <tr class='highlight-red'><td>Monthly Take-Home Salary</td><td>{format_currency(take_home)}</td></tr>
    </table>
    """, unsafe_allow_html=True)