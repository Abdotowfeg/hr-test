# -*- coding: utf-8 -*-
{
    'name': 'Employee Loan Management (Saudi)',
    'version': '15.0',
    'summary': 'Manage Loan Requests',
    'description': """
        Helps you to manage Loan Requests of your company's staff.
        """,
    'category': 'Generic Modules/Human Resources',
    'author': "",
    'depends': [
        'base', 'hr_payroll_extension', 'hr_employee_extension', 'account',
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/hr_loan.xml',
        'views/hr_loan_seq.xml',
        'data/salary_rule_loan.xml',
        'views/hr_loan_acc.xml',
        'views/hr_payroll.xml',
        'views/hr_loan_config.xml'
    ],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
