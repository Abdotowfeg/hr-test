# -*- coding: utf-8 -*-

{
    'name': 'Hr Overtime (Saudi)',
    'version': '15.0',
    'summary': 'Manage Employee Overtime',
    'description': """
        Helps you to manage Employee Overtime.
        """,
    'category': 'Generic Modules/Human Resources',
    'author': "",
    'depends': [
        'hr_employee_extension', 'hr_contract', 'hr_attendance', 'hr_holidays', 'hr_payroll_extension'
    ],
   
    'data': [

        'data/data.xml',
        'views/overtime_request_view.xml',
        'views/overtime_type.xml',
        'views/hr_contract.xml',
        # 'views/hr_payslip.xml',
        'security/ir.model.access.csv',
    ],
    'demo': ['data/hr_overtime_demo.xml'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
