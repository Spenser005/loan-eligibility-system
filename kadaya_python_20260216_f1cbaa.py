import pandas as pd
import numpy as np
from datetime import datetime

class LoanEligibilityChecker:
    def __init__(self):
        self.eligibility_criteria = {
            'min_age': 21,
            'max_age': 65,
            'min_income': 15000,
            'min_credit_score': 650,
            'min_employment_years': 1,
            'max_dti_ratio': 0.43,  # Debt-to-Income ratio
            'min_down_payment_pct': 0.05  # 5% minimum down payment
        }
    
    def check_eligibility(self, applicant):
        """Check if applicant meets basic eligibility criteria"""
        results = {
            'eligible': True,
            'reasons': [],
            'score': 0,
            'max_loan_amount': 0
        }
        
        # Age check
        if applicant['age'] < self.eligibility_criteria['min_age']:
            results['eligible'] = False
            results['reasons'].append(f"Age below minimum ({self.eligibility_criteria['min_age']})")
        elif applicant['age'] > self.eligibility_criteria['max_age']:
            results['eligible'] = False
            results['reasons'].append(f"Age above maximum ({self.eligibility_criteria['max_age']})")
        
        # Income check
        if applicant['annual_income'] < self.eligibility_criteria['min_income']:
            results['eligible'] = False
            results['reasons'].append(f"Income below minimum (${self.eligibility_criteria['min_income']})")
        
        # Credit score check
        if applicant['credit_score'] < self.eligibility_criteria['min_credit_score']:
            results['eligible'] = False
            results['reasons'].append(f"Credit score below minimum ({self.eligibility_criteria['min_credit_score']})")
        
        # Employment check
        if applicant['employment_years'] < self.eligibility_criteria['min_employment_years']:
            results['eligible'] = False
            results['reasons'].append(f"Employment period below minimum ({self.eligibility_criteria['min_employment_years']} years)")
        
        # Calculate debt-to-income ratio
        monthly_income = applicant['annual_income'] / 12
        monthly_debt = applicant.get('monthly_debt', 0)
        dti_ratio = monthly_debt / monthly_income if monthly_income > 0 else 1
        
        if dti_ratio > self.eligibility_criteria['max_dti_ratio']:
            results['eligible'] = False
            results['reasons'].append(f"Debt-to-income ratio too high ({dti_ratio:.2%})")
        
        # Calculate eligibility score (0-100)
        if results['eligible']:
            results['score'] = self.calculate_eligibility_score(applicant)
            results['max_loan_amount'] = self.calculate_max_loan(applicant)
        
        return results
    
    def calculate_eligibility_score(self, applicant):
        """Calculate eligibility score based on various factors"""
        score = 0
        
        # Credit score contribution (0-40 points)
        credit_score = applicant['credit_score']
        if credit_score >= 800:
            score += 40
        elif credit_score >= 750:
            score += 35
        elif credit_score >= 700:
            score += 30
        elif credit_score >= 650:
            score += 25
        else:
            score += 20
        
        # Income contribution (0-30 points)
        income = applicant['annual_income']
        if income >= 100000:
            score += 30
        elif income >= 75000:
            score += 25
        elif income >= 50000:
            score += 20
        elif income >= 30000:
            score += 15
        else:
            score += 10
        
        # Employment stability (0-20 points)
        employment_years = applicant['employment_years']
        if employment_years >= 10:
            score += 20
        elif employment_years >= 5:
            score += 15
        elif employment_years >= 3:
            score += 10
        elif employment_years >= 1:
            score += 5
        
        # Down payment contribution (0-10 points)
        down_payment_pct = applicant.get('down_payment_pct', 0)
        if down_payment_pct >= 0.2:
            score += 10
        elif down_payment_pct >= 0.1:
            score += 7
        elif down_payment_pct >= 0.05:
            score += 5
        
        return min(score, 100)  # Cap at 100
    
    def calculate_max_loan(self, applicant):
        """Calculate maximum loan amount"""
        # Simple calculation based on income and credit score
        income_multiplier = 3  # Standard multiplier
        if applicant['credit_score'] >= 750:
            income_multiplier = 4
        elif applicant['credit_score'] >= 700:
            income_multiplier = 3.5
        
        max_loan = applicant['annual_income'] * income_multiplier
        
        # Adjust for existing debt
        monthly_debt = applicant.get('monthly_debt', 0)
        if monthly_debt > 0:
            max_loan -= (monthly_debt * 12) * 2  # Reduce by 2 years of debt
        
        return max(max_loan, 0)