# Take-Home Salary Calculator (FY 2025-26)

This is a **Streamlit-based Salary Calculator** that calculates monthly take-home salary, total tax payable, and bonus take-home based on the new tax regime for **FY 2025-26**.

## Features
- **Dynamic Salary Selection**: Adjust base salary and bonus percentage using sliders.
- **Tax Calculation as per FY 2025-26**: Includes standard deduction, income tax slabs, surcharge, and cess.
- **Bonus Taxation**: Computes annual bonus and take-home bonus after tax.
- **Employer & Employee PF Contributions**: Calculates monthly and annual Provident Fund contributions.
- **Clean & Professional UI**: Displays results in a structured table format with key metrics highlighted.

## Installation & Setup
### 1. Install Dependencies
Ensure you have Python installed, then install the required dependencies:
```sh
pip install streamlit
```

### 2. Run the Application
Execute the following command to start the app:
```sh
streamlit run take_home_salary_calc.py
```

## How It Works
1. **Select Base Salary**: Adjust the slider to set the base annual salary.
2. **Choose Bonus Percentage**: Define the bonus percentage using the slider.
3. **View Results**:
   - **Annual Bonus**
   - **Employer PF Retirals (6% of base salary)**
   - **Total CTC (Base Salary + Bonus + Employer PF)**
   - **Annual Tax Payable**
   - **Annual Bonus (Take Home after Tax Deduction)**
   - **Monthly PF Contribution (Employee + Employer)**
   - **Monthly Take-Home Salary**

## Example Output
If a user selects **Base Salary = ₹15L & Bonus = 16%**, the calculator will output:
```
Annual Bonus: ₹2,40,000.00
PF Retirals (Employer): ₹90,000.00
Total CTC: ₹16,80,000.00
Annual Tax Payable: ₹1,10,500.00
Annual Bonus (Take Home): ₹2,10,000.00
Monthly PF Contribution (Employee + Employer): ₹15,000.00
Monthly Take-Home Salary: ₹1,10,500.00
```

## License
This project is open-source and available under the MIT License.